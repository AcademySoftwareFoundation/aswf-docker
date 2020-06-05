# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
GroupInfo
"""
import typing
import logging

from aswfdocker import constants, utils, index

logger = logging.getLogger(__name__)


class GroupInfo:
    """Image Group Info
    An image group is a group of related docker images that will be built together.
    """

    def __init__(
        self,
        type_: constants.ImageType,
        names: typing.List[str],
        versions: typing.List[str],
        target: str = "",
    ):
        self.index = index.Index()
        self.type = type_
        self.names = names
        self.versions = versions
        for name in self.names:
            if name not in constants.GROUPS[self.type]:
                raise TypeError(f"Group {name} is not valid!")
        self.images = []
        for images in [constants.GROUPS[self.type][n] for n in self.names]:
            self.images.extend(images)
        self.target = target

    def iter_images_versions(self):
        for image in self.images:
            if self.target and image != self.target:
                logger.debug("Skipping target %s", image)
                continue
            logger.debug("release image=%s", image)
            all_versions = list(self.index.iter_versions(self.type, image))
            major_versions = [utils.get_major_version(v) for v in all_versions]
            for version in [v for v in self.versions if v in major_versions]:
                logger.debug("release version=%s", version)
                version = all_versions[major_versions.index(version)]
                yield image, version
