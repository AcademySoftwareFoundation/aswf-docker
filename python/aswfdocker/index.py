# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Index of docker images and versions.
"""
import os

import yaml

from aswfdocker import constants, utils, versioninfo


class Index:
    """
    This is the index of all current package, images and versions.
    The data comes from the "versions.yaml" file at the root of the git repository.
    """

    def __init__(self):
        versions_file_path = os.path.join(utils.get_git_top_level(), "versions.yaml")
        with open(versions_file_path) as f:
            self._versions = yaml.load(f, Loader=yaml.FullLoader)

    def _get_key(self, image_type: constants.ImageType):
        if image_type == constants.ImageType.PACKAGE:
            return "ci-packages"
        return "ci-images"

    def iter_images(self, image_type: constants.ImageType):
        """
        Iterates over all images by image type.
        """
        for image in self._versions[self._get_key(image_type)]:
            yield image

    def iter_versions(self, image_type: constants.ImageType, name: str):
        """
        Iterates over all versions by image type and image name.
        """
        for version in self._versions[self._get_key(image_type)][name]:
            yield version

    def iter_version_info(self):
        for v in self._versions["versions"]:
            yield versioninfo.VersionInfo(
                version=v.get("version"),
                major_version=v.get("major_version"),
                tags=v.get("tags", []),
                ci_common_version=v.get("ci_common_version"),
                python_version=v.get("python_version"),
                dts_version=v.get("dts_version"),
                clang_major_version=v.get("clang_major_version"),
                use_major_version_as_tag=v.get("use_major_version_as_tag", True),
            )

    def version_info(self, version):
        for vi in self.iter_version_info():
            if version == vi.version:
                return vi
        raise ValueError("VersionInfo not found for version {}".format(version))
