# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
GroupInfo
"""
import typing
from aswfdocker import constants


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
