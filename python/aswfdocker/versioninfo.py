# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Docker Image Version information
"""
import typing
from aswfdocker import constants


class VersionInfo:
    """
    Docker image version information for use in builder
    """

    def __init__(  # noqa too many arguments
        self,
        version: str,
        major_version: str,
        tags: typing.List[str],
        ci_common_version: str,
        python_version: str,
        dts_version: str,
        clang_major_version: str,
        use_major_version_as_tag=True,
        cuda_version: str,
    ):
        self.version = version
        self.major_version = major_version
        self.ci_common_version = ci_common_version
        self.tags = tags
        self.python_version = python_version
        self.dts_version = dts_version
        self.clang_major_version = clang_major_version
        self.use_major_version_as_tag = use_major_version_as_tag
        self.cuda_version = cuda_version

    def get_tags(
        self, aswf_version: str, docker_org: str, image_name: str
    ) -> typing.List[str]:
        if self.use_major_version_as_tag:
            tags = [self.major_version]
            if self.major_version != self.version:
                tags.append(self.version)
        else:
            tags = [self.version]
        tags.append(aswf_version)
        tags.extend(self.tags)

        return list(
            map(
                lambda tag: f"{constants.DOCKER_REGISTRY}/{docker_org}/{image_name}:{tag}",
                tags,
            )
        )
