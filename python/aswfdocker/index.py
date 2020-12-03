# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Index of Docker images and versions.
"""
import logging
import yaml
import importlib_resources

from aswfdocker import constants, versioninfo

logger = logging.getLogger(__name__)


class Index:
    """
    This is the index of all current package, images and versions.
    The data comes from the "versions.yaml" file at the root of the git repository.
    """

    def __init__(self):
        with importlib_resources.files("aswfdocker.data").joinpath(
            "versions.yaml"
        ).open() as f:
            self._versions = yaml.load(f, Loader=yaml.FullLoader)
        self.groups = {
            constants.ImageType.IMAGE: self._versions["groups"]["image"],
            constants.ImageType.PACKAGE: self._versions["groups"]["package"],
        }
        self._version_infos = {}
        for version, v in self._versions["versions"].items():
            self._version_infos[version] = versioninfo.VersionInfo(
                version=version,
                major_version=v.get("major_version"),
                tags=v.get("tags", []),
                ci_common_version=v.get("ci_common_version"),
                package_versions=v.get("package_versions", {}),
                parent_versions=v.get("parent_versions", []),
                use_major_version_as_tag=v.get("use_major_version_as_tag", False),
            )
        for vi in self._version_infos.values():
            vi.all_package_versions = vi.package_versions.copy()
            for parent in vi.parent_versions:
                vi.all_package_versions.update(
                    self._version_infos[parent].package_versions
                )

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
        return self._version_infos.values()

    def version_info(self, version):
        for vi in self.iter_version_info():
            if version == vi.version:
                return vi
        raise ValueError("VersionInfo not found for version {}".format(version))

    def package_data(self, package_name):
        return self._versions["package_data"].get(package_name, {})

    def get_group_from_image(self, image_type: constants.ImageType, image: str):
        for group, images in self.groups[image_type].items():
            for img in images:
                if img == image:
                    return group
        raise RuntimeError(f"Cannot find group for image {image}")
