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
    An image group is a group of related Docker images that will be built together.
    """

    def __init__(
        self,
        type_: constants.ImageType,
        names: typing.List[str],
        versions: typing.List[str],
        targets: typing.List[str],
    ):
        self.index = index.Index()
        self.type = type_
        self.names = names
        for name in self.names:
            if name not in self.index.groups[self.type]:
                raise TypeError(f"Group {name} is not valid!")
        self.images = []
        for images in [self.index.groups[self.type][n] for n in self.names]:
            self.images.extend(images)
        if not versions or (len(versions) == 1 and versions[0] == constants.ALL):
            version_set = set()
            for image in self.images:
                for v in self.index.iter_versions(self.type, image):
                    version_set.add(utils.get_major_version(v))
            versions = sorted(version_set)
        self.versions = [utils.get_major_version(v) for v in sorted(versions)]
        self.targets = targets
        logger.debug(
            "GroupInfo: type=%s names=%s versions=%s images=%s targets=%s",
            self.type,
            self.names,
            self.versions,
            self.images,
            self.targets,
        )

    def iter_images_versions(self, get_image=False):
        for image in self.images:
            if self.targets and image not in self.targets:
                logger.debug("Skipping target %s", image)
                continue
            ci_image = utils.get_image_name(self.type, image)
            all_versions = list(self.index.iter_versions(self.type, image))
            major_versions = [utils.get_major_version(v) for v in all_versions]
            logger.debug(
                "iter image=%s ci_image=%s all_versions=%s",
                image,
                ci_image,
                all_versions,
            )
            for version in [v for v in self.versions if v in major_versions]:
                logger.debug("iter version=%s", version)
                version = all_versions[major_versions.index(version)]
                if get_image:
                    yield image, version
                else:
                    yield ci_image, version
