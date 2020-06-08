# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Main configuration and constants for aswfdocker
"""
import enum

from aswfdocker import versioninfo


class ImageType(enum.Enum):
    IMAGE = "image"
    PACKAGE = "package"


# Groups try to split builds into reasonable blocks of build time
GROUPS = {
    ImageType.PACKAGE: {
        "common": ["clang", "ninja"],
        "base1": ["python", "boost", "tbb", "cppunit", "glew", "glfw", "log4cplus"],
        "base2": ["qt"],
        "base3": ["pyside"],
        "vfx1": ["blosc", "openexr", "alembic", "ocio", "oiio"],
        "vfx2": ["opensubdiv", "ptex", "openvdb", "usd"],
        "vfx3": ["partio", "osl"],
    },
    ImageType.IMAGE: {
        "common": ["common"],
        "base": ["base"],
        "vfx1": ["openexr", "openvdb", "opencue"],
        "vfx2": ["ocio", "osl"],
        "usd": ["usd"],
        "vfxall": ["vfxall"],
    },
}

VERSION_INFO = {
    "1": versioninfo.VersionInfo(
        major_version="1",
        label="latest",
        ci_common_version="1",
        python_version="2.7",
        dts_version="6",
    ),
    "2": versioninfo.VersionInfo(
        major_version="2",
        label="preview",
        ci_common_version="2",
        python_version="3.7",
        dts_version="9",
    ),
    "2018": versioninfo.VersionInfo(
        major_version="2018",
        label=None,
        ci_common_version="1",
        python_version="2.7",
        dts_version="6",
    ),
    "2019": versioninfo.VersionInfo(
        major_version="2019",
        label="latest",
        ci_common_version="1",
        python_version="2.7",
        dts_version="6",
    ),
    "2020": versioninfo.VersionInfo(
        major_version="2020",
        label="preview",
        ci_common_version="1",
        python_version="3.7",
        dts_version="6",
    ),
    "2021": versioninfo.VersionInfo(
        major_version="2021",
        label="alpha",
        ci_common_version="2",
        python_version="3.7",
        dts_version="9",
    ),
}

PUBLISH_DOCKER_ORG = "aswf"
TESTING_DOCKER_ORG = "aswftesting"
# this org is not valid, but this ensures that the test will not accidently pull an existing image
FAKE_DOCKER_ORG = "aswflocaltesting"

DOCKER_REGISTRY = "docker.io"

DEV_BUILD_DATE = "dev"
DEV_VCS_REF = "dev"

MAIN_GITHUB_ASWF_ORG = "AcademySoftwareFoundation"
MAIN_GITHUB_REPO_NAME = "aswf-docker"
MAIN_GITHUB_ASWF_DOCKER_URL = (
    f"https://github.com/{MAIN_GITHUB_ASWF_ORG}/{MAIN_GITHUB_REPO_NAME}"
)

IMAGE_NAME_REGEX = r"(refs/tags/)?(?P<org>[a-z]+)/ci-(?P<package>package\-)?(?P<image>[a-z0-9]+)[:/](?P<version>[0-9\.]+)"
