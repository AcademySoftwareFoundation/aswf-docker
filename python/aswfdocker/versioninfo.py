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
        parent_versions: typing.List[str],
        package_versions: typing.Dict[str, str],
        use_major_version_as_tag=True,
    ):
        self.version = version
        self.major_version = major_version
        self.ci_common_version = ci_common_version
        self.tags = tags
        self.parent_versions = parent_versions
        self.package_versions = package_versions
        self.use_major_version_as_tag = use_major_version_as_tag
        self.all_package_versions: typing.Dict[str, str] = {}

    def get_tags(
        self,
        aswf_version: str,
        docker_org: str,
        image_name: str,
        extra_suffix: typing.Optional[str] = None,
    ) -> typing.List[str]:
        if self.use_major_version_as_tag:
            tags = [self.major_version]
            if self.major_version != self.version:
                tags.append(self.version)
        else:
            tags = [self.version]
        tags.append(aswf_version)
        tags.extend(self.tags)
        if extra_suffix:
            tags.append(self.major_version + "-" + extra_suffix)

        return list(
            map(
                lambda tag: f"{constants.DOCKER_REGISTRY}/{docker_org}/{image_name}:{tag}",
                tags,
            )
        )
