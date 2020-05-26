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
        major_version: str,
        label: typing.Optional[str],
        ci_common_version: str,
        python_version: str,
        dts_version: str,
    ):
        self.major_version = major_version
        self.ci_common_version = ci_common_version
        self.label = label
        self.python_version = python_version
        self.dts_version = dts_version

    def get_tags(
        self, aswf_version: str, docker_org: str, image_name: str
    ) -> typing.List[str]:
        tags = [
            self.major_version,
            aswf_version,
        ]
        if self.label:
            tags.append(self.label)
        return list(
            map(
                lambda tag: f"{constants.DOCKER_REGISTRY}/{docker_org}/{image_name}:{tag}",
                tags,
            )
        )
