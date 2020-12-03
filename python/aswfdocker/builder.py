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
    """Builder generates a "docker buildx bake" json file to drive the parallel builds of Docker images.
    """

    def __init__(
        self,
        build_info: aswfinfo.ASWFInfo,
        group_info: groupinfo.GroupInfo,
        push: bool = False,
    ):
        self.push = push
        self.build_info = build_info
        self.group_info = group_info
        self.index = index.Index()

    def make_bake_dict(self) -> typing.Dict[str, dict]:
        root: typing.Dict[str, dict] = {}
        root["target"] = {}
        for image, version in self.group_info.iter_images_versions():
            major_version = utils.get_major_version(version)
            version_info = self.index.version_info(major_version)
            if self.group_info.type == constants.ImageType.PACKAGE:
                tags = version_info.get_tags(
                    version,
                    self.build_info.docker_org,
                    image,
                    extra_suffix=version_info.package_versions.get(
                        "ASWF_" + image.replace("ci-package-", "").upper() + "_VERSION"
                    ),
                )
                docker_file = f"packages/{self.index.get_group_from_image(self.group_info.type, image.replace('ci-package-', ''))}/Dockerfile"
            else:
                tags = version_info.get_tags(version, self.build_info.docker_org, image)
                docker_file = f"{image}/Dockerfile"
            target_dict = {
                "context": ".",
                "dockerfile": docker_file,
                "args": {
                    "ASWF_ORG": self.build_info.docker_org,
                    "ASWF_PKG_ORG": self.build_info.package_org,
                    "ASWF_VERSION": version,
                    "CI_COMMON_VERSION": version_info.ci_common_version,
                    "ASWF_VFXPLATFORM_VERSION": version_info.major_version,
                },
                "labels": {
                    "org.opencontainers.image.created": self.build_info.build_date,
                    "org.opencontainers.image.revision": self.build_info.vcs_ref,
                },
                "tags": tags,
                "output": ["type=registry,push=true" if self.push else "type=docker"],
            }
            target_dict["args"].update(version_info.all_package_versions)
            if self.group_info.type == constants.ImageType.PACKAGE:
                target_dict["target"] = image
            root["target"][f"{image}-{major_version}"] = target_dict

        root["group"] = {"default": {"targets": list(root["target"].keys())}}
        return root

    def make_bake_jsonfile(self) -> str:
        d = self.make_bake_dict()
        path = os.path.join(
            tempfile.gettempdir(),
            f"docker-bake-{self.group_info.type.name}-{'-'.join(self.group_info.names)}-{'-'.join(self.group_info.versions)}.json",
        )
        with open(path, "w") as f:
            json.dump(d, f, indent=4, sort_keys=True)
        return path

    def build(self, dry_run: bool = False, progress: str = "") -> None:
        path = self.make_bake_jsonfile()
        cmd = f"docker buildx bake -f {path} --progress {progress}"
        logger.debug("Repo root: %s", self.build_info.repo_root)
        if dry_run:
            logger.info("Would build: %r", cmd)
        else:
            logger.info("Building: %r", cmd)
            subprocess.run(cmd, shell=True, check=True, cwd=self.build_info.repo_root)
