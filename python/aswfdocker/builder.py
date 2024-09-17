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

    def make_bake_dict(
        self,
        keep_source: bool,
        keep_build: bool,
        build_missing: bool,
    ) -> typing.Dict[str, dict]:
        # pylint: disable=too-many-locals
        root: typing.Dict[str, dict] = {}
        root["target"] = {}
        for image, version in self.group_info.iter_images_versions():
            use_conan = self.group_info.type == constants.ImageType.PACKAGE and (
                self.use_conan
                or self.index.is_conan_only_package(image.replace("ci-package-", ""))
            )
            versions_to_bake = set()
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
                    # if version_info.ci_common_version != major_version:
                    # Only bake conan images in ci_common container!
                    # version = version_info.ci_common_version
                    # major_version = utils.get_major_version(version)
                    versions_to_bake.add(version)
                    tags = list(
                        map(
                            lambda tag: f"{constants.DOCKER_REGISTRY}/{self.build_info.docker_org}"
                            + f"/ci-baseos-gl-conan:{tag}",
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

            major_version_no_clang = major_version.split("-")[0]
            if version_info.ci_common_version == major_version_no_clang:
                channel = f"ci_common{major_version_no_clang}"
            else:
                channel = f"vfx{version_info.major_version}"
            args = {
                "ASWF_ORG": self.build_info.docker_org,
                "ASWF_PKG_ORG": self.build_info.package_org,
                "ASWF_VERSION": version,
                "CI_COMMON_VERSION": version_info.ci_common_version,
                "ASWF_CONAN_CHANNEL": channel,
            }
            if use_conan:
                # params as env var needed for conan build
                args.update(
                    {
                        "ASWF_PKG_NAME": image.replace("ci-package-", ""),
                        "ASWF_PKG_VERSION": version_info.package_versions.get(
                            "ASWF_"
                            # Handle dependencies with hyhpen in their name.
                            + image.replace("ci-package-", "").upper().replace("-", "_")
                            + "_VERSION"
                        ),
                        "CONAN_USER_HOME": constants.CONAN_USER_HOME,
                        "ASWF_CONAN_KEEP_SOURCE": "--keep-source"
                        if keep_source
                        else "",
                        "ASWF_CONAN_KEEP_BUILD": "--keep-build" if keep_build else "",
                        "ASWF_CONAN_BUILD_MISSING": "--build=missing"
                        if build_missing
                        else "",
                        "ASWF_CONAN_PUSH": "TRUE" if self.push else "",
                    }
                )
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
                    target_dict["target"] = "ci-baseos-gl-conan"
                else:
                    target_dict["target"] = image
            root["target"][f"{image}-{major_version}"] = target_dict

        root["group"] = {"default": {"targets": list(root["target"].keys())}}
        return root

    def make_bake_jsonfile(
        self,
        keep_source: bool,
        keep_build: bool,
        build_missing: bool,
    ) -> typing.Optional[str]:
        d = self.make_bake_dict(keep_source, keep_build, build_missing)
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
            envs["CONAN_LOGIN_USERNAME"] = os.environ["CONAN_LOGIN_USERNAME"]
        if "ARTIFACTORY_USER" in os.environ:
            envs["CONAN_LOGIN_USERNAME"] = os.environ["ARTIFACTORY_USER"]
        if "CONAN_PASSWORD" in os.environ:
            envs["CONAN_PASSWORD"] = os.environ["CONAN_PASSWORD"]
        if "ARTIFACTORY_TOKEN" in os.environ:
            envs["CONAN_PASSWORD"] = os.environ["ARTIFACTORY_TOKEN"]
        for name, value in version_info.all_package_versions.items():
            envs[name] = value
        return envs

    # We should leverage this to avoid repeating volume definitions in packages/common/Dockerfiles
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
            + f"/ci-baseos-gl-conan:{version_info.ci_common_version}"
        )
        base_cmd.append(tag)
        return base_cmd

    def _build_conan_package(
        self,
        image,
        version,
        dry_run,
        progress,
        conan_login,
        bake_jsonfile,
    ):
        # pylint: disable=consider-using-f-string
        major_version = utils.get_major_version(version)
        version_info = self.index.version_info(major_version)
        base_cmd = self._get_conan_base_cmd(version_info)
        if conan_login:
            # We keep this as a separate step: the end result is to store credentials in
            # packages/conan/.conan/.conan.db which is not thread safe: once we are able
            # to run Conan builds from a single "docker buildx bake" invocation, we will
            # want to keep the login step separate.
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
        #
        # These are kept for reference, they now live in
        # packages/common/Dockerfile
        #
        # full_version = version_info.package_versions.get(
        #    "ASWF_" + image.upper() + "_VERSION"
        # )
        # conan_version = (
        #    f"{image}/{full_version}"
        #    f"@{self.build_info.docker_org}/{version_info.conan_profile}"
        # )
        # alias_version = (
        #    f"{image}/latest"
        #    f"@{self.build_info.docker_org}/{version_info.conan_profile}"
        # )

        # buildx bake --set allows us to override settings in the bake file and avoid having
        #   to rewrite it.
        # output=type=cacheonly : no container is produced, we only want the cache containing
        #   the output of conan builds
        # target.target=ci-conan-package-builder : see packages/common/Dockerfile for the Conan
        #   build container which runs:
        #
        # - conan user (conditional)
        # - conan create
        # - conan alias
        # - conan upload main version (conditional)
        # - conan upload latest alias version (conditional)
        #
        # not sure about ci-package-{image}-{major_version}
        #
        # Make pylint / pytest happy, they get confused by f-string
        runcmd = (
            "docker buildx bake -f {} --set=*.output=type=cacheonly "
            "--set=*.target.target=ci-conan-package-builder --progress {} "
            "ci-package-{}-{}".format(bake_jsonfile, progress, image, major_version)
        )

        self._run(
            runcmd,
            dry_run=dry_run,
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

        path = self.make_bake_jsonfile(keep_source, keep_build, build_missing)
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
                progress,
                conan_login,
                path,
            )
