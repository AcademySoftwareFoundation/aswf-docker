# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
CI Image and Package Builder
"""
import logging
import subprocess
import json
import os
import tempfile
import typing

from aswfdocker import constants, aswfinfo, utils, groupinfo, index

logger = logging.getLogger(__name__)


class Builder:
    """Builder generates a "docker buildx bake" json file to drive the parallel builds of Docker images."""

    def __init__(
        self,
        build_info: aswfinfo.ASWFInfo,
        group_info: groupinfo.GroupInfo,
        push: bool = False,
        use_conan: bool = False,
    ):
        self.push = push
        self.build_info = build_info
        self.group_info = group_info
        self.use_conan = use_conan
        self.index = index.Index()

    def make_bake_dict(self) -> typing.Dict[str, dict]:
        root: typing.Dict[str, dict] = {}
        root["target"] = {}
        versions_to_bake = set()
        for image, version in self.group_info.iter_images_versions():
            use_conan = self.group_info.type == constants.ImageType.PACKAGE and (
                self.use_conan
                or self.index.is_conan_only_package(image.replace("ci-package-", ""))
            )
            major_version = utils.get_major_version(version)
            version_info = self.index.version_info(major_version)
            if self.group_info.type == constants.ImageType.PACKAGE:
                image_base = image.replace("ci-package-", "")
                group = self.index.get_group_from_image(
                    self.group_info.type, image_base
                )
                if use_conan:
                    if version in versions_to_bake:
                        # Only one version per image needed
                        continue
                    if version_info.ci_common_version != major_version:
                        # Only bake images for ci_common!
                        version = version_info.ci_common_version
                        major_version = utils.get_major_version(version)
                    versions_to_bake.add(version)
                    tags = list(
                        map(
                            lambda tag: f"{constants.DOCKER_REGISTRY}/{self.build_info.docker_org}"
                            + f"/ci-centos7-gl-conan:{tag}",
                            [version, major_version],
                        )
                    )
                    docker_file = "packages/common/Dockerfile"
                else:
                    tags = version_info.get_tags(
                        version,
                        self.build_info.docker_org,
                        image,
                        extra_suffix=version_info.package_versions.get(
                            "ASWF_"
                            + image.replace("ci-package-", "").upper()
                            + "_VERSION"
                        ),
                    )
                    docker_file = f"packages/{group}/Dockerfile"
            else:
                tags = version_info.get_tags(version, self.build_info.docker_org, image)
                docker_file = f"{image}/Dockerfile"

            if version_info.ci_common_version == major_version:
                channel = f"ci_common{major_version}"
            else:
                channel = f"vfx{version_info.major_version}"
            args = {
                "ASWF_ORG": self.build_info.docker_org,
                "ASWF_PKG_ORG": self.build_info.package_org,
                "ASWF_VERSION": version,
                "CI_COMMON_VERSION": version_info.ci_common_version,
                "ASWF_CONAN_CHANNEL": channel,
            }
            args.update(version_info.all_package_versions)
            target_dict = {
                "context": ".",
                "dockerfile": docker_file,
                "args": args,
                "labels": {
                    "org.opencontainers.image.created": self.build_info.build_date,
                    "org.opencontainers.image.revision": self.build_info.vcs_ref,
                },
                "tags": tags,
                "output": ["type=registry,push=true" if self.push else "type=docker"],
            }
            if self.group_info.type == constants.ImageType.PACKAGE:
                if use_conan:
                    target_dict["target"] = "ci-centos7-gl-conan"
                else:
                    target_dict["target"] = image
            root["target"][f"{image}-{major_version}"] = target_dict

        root["group"] = {"default": {"targets": list(root["target"].keys())}}
        return root

    def make_bake_jsonfile(self) -> typing.Optional[str]:
        d = self.make_bake_dict()
        if not d["group"]["default"]["targets"]:
            return None
        groups = "-".join(self.group_info.names)
        versions = "-".join(self.group_info.versions)
        path = os.path.join(
            tempfile.gettempdir(),
            f"docker-bake-{self.group_info.type.name}-{groups}-{versions}.json",
        )
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=4, sort_keys=True)
        return path

    def _run(self, cmd: str, dry_run: bool):
        if dry_run:
            logger.info("Would run: '%s'", cmd)
        else:
            logger.info("Building: '%s'", cmd)
            subprocess.run(cmd, shell=True, check=True, cwd=self.build_info.repo_root)

    def _run_in_docker(self, base_cmd, cmd, dry_run):
        self._run(
            " ".join(base_cmd + cmd),
            dry_run=dry_run,
        )

    def _get_conan_env_vars(self, version_info):
        envs = {
            "CONAN_USER_HOME": constants.CONAN_USER_HOME,
            "CCACHE_DIR": "/tmp/ccache",
            "CONAN_NON_INTERACTIVE": "1",
        }
        if "CONAN_LOGIN_USERNAME" in os.environ:
            envs["CONAN_LOGIN_USERNAME"] = os.environ["CONAN_PASSWORD"]
        if "ARTIFACTORY_USER" in os.environ:
            envs["CONAN_LOGIN_USERNAME"] = os.environ["ARTIFACTORY_USER"]
        if "CONAN_PASSWORD" in os.environ:
            envs["CONAN_PASSWORD"] = os.environ["CONAN_PASSWORD"]
        if "ARTIFACTORY_TOKEN" in os.environ:
            envs["CONAN_PASSWORD"] = os.environ["ARTIFACTORY_TOKEN"]
        for name, value in version_info.all_package_versions.items():
            envs[name] = value
        return envs

    def _get_conan_vols(self):
        conan_base = os.path.join(utils.get_git_top_level(), "packages", "conan")
        vols = {
            os.path.join(conan_base, "settings"): os.path.join(
                constants.CONAN_USER_HOME, ".conan"
            ),
            os.path.join(conan_base, "data"): os.path.join(
                constants.CONAN_USER_HOME, "d"
            ),
            os.path.join(conan_base, "recipes"): os.path.join(
                constants.CONAN_USER_HOME, "recipes"
            ),
            os.path.join(conan_base, "ccache"): "/tmp/ccache",
        }
        return vols

    def _get_conan_base_cmd(self, version_info):
        base_cmd = ["docker", "run"]
        for name, value in self._get_conan_env_vars(version_info).items():
            base_cmd.append("-e")
            base_cmd.append(f"{name}={value}")
        for name, value in self._get_conan_vols().items():
            base_cmd.append("-v")
            base_cmd.append(f"{name}:{value}")
        tag = (
            f"{constants.DOCKER_REGISTRY}/{self.build_info.docker_org}"
            + f"/ci-centos7-gl-conan:{version_info.ci_common_version}"
        )
        base_cmd.append(tag)
        return base_cmd

    def _build_conan_package(
        self,
        image,
        version,
        dry_run,
        keep_source,
        keep_build,
        conan_login,
        build_missing,
    ):
        major_version = utils.get_major_version(version)
        version_info = self.index.version_info(major_version)
        base_cmd = self._get_conan_base_cmd(version_info)
        if conan_login:
            self._run_in_docker(
                base_cmd,
                [
                    "conan",
                    "user",
                    "-p",
                    "-r",
                    self.build_info.docker_org,
                ],
                dry_run,
            )
        self._run_in_docker(
            base_cmd,
            [
                "conan",
                "config",
                "set",
                f"general.default_profile={version_info.conan_profile}",
            ],
            dry_run,
        )
        full_version = version_info.package_versions.get(
            "ASWF_" + image.upper() + "_VERSION"
        )
        conan_version = (
            f"{image}/{full_version}"
            f"@{self.build_info.docker_org}/{version_info.conan_profile}"
        )
        build_cmd = [
            "conan",
            "create",
            os.path.join(constants.CONAN_USER_HOME, "recipes", image),
            conan_version,
        ]
        if keep_source:
            build_cmd.append("--keep-source")
        if keep_build:
            build_cmd.append("--keep-build")
        if build_missing:
            build_cmd.append("--build=missing")
        self._run_in_docker(
            base_cmd,
            build_cmd,
            dry_run,
        )
        alias_version = (
            f"{image}/latest"
            f"@{self.build_info.docker_org}/{version_info.conan_profile}"
        )
        self._run_in_docker(
            base_cmd,
            [
                "conan",
                "alias",
                alias_version,
                conan_version,
            ],
            dry_run,
        )
        if self.push:
            self._run_in_docker(
                base_cmd,
                [
                    "conan",
                    "upload",
                    "--all",
                    "-r",
                    self.build_info.docker_org,
                    conan_version,
                ],
                dry_run,
            )
            self._run_in_docker(
                base_cmd,
                [
                    "conan",
                    "upload",
                    "--all",
                    "-r",
                    self.build_info.docker_org,
                    alias_version,
                ],
                dry_run,
            )

    def build(
        self,
        dry_run: bool = False,
        progress: str = "",
        keep_source=False,
        keep_build=False,
        conan_login=False,
        build_missing=False,
    ) -> None:
        images_and_versions = []
        for image, version in self.group_info.iter_images_versions(get_image=True):
            if (
                self.group_info.type == constants.ImageType.PACKAGE
                and not self.use_conan
                and self.index.is_conan_only_package(image)
            ):
                logger.warning("Skipping %s as it is a conan-only package!", image)
                continue
            images_and_versions.append((image, version))

        if not images_and_versions:
            return

        path = self.make_bake_jsonfile()
        if path:
            self._run(
                f"docker buildx bake -f {path} --progress {progress}", dry_run=dry_run
            )
        if not self.use_conan or self.group_info.type == constants.ImageType.IMAGE:
            return

        conan_base = os.path.join(utils.get_git_top_level(), "packages", "conan")
        for image, version in images_and_versions:
            recipe_path = os.path.join(conan_base, "recipes", image)
            if not os.path.exists(recipe_path):
                logger.warning("Recipe for %s not found: skipping!", image)
                continue
            self._build_conan_package(
                image,
                version,
                dry_run,
                keep_source,
                keep_build,
                conan_login,
                build_missing,
            )
