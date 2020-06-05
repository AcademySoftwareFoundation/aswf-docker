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


GROUPS = {
    ImageType.PACKAGE: {
        "common": ["clang", "ninja"],
        "base": ["python", "boost", "tbb", "cppunit", "glew", "glfw", "log4cplus"],
        "baseqt": ["qt"],
        "basepyside": ["pyside"],
        "vfx": [
            "blosc",
            "openexr",
            "alembic",
            "ocio",
            "oiio",
            "opensubdiv",
            "ptex",
            "openvdb",
            "usd",
            "partio",
            "osl",
        ],
    },
    ImageType.IMAGE: {
        "common": ["common"],
        "base": ["base"],
        "openexr": ["openexr"],
        "openvdb": ["openvdb"],
        "osl": ["osl"],
        "opencue": ["opencue"],
        "ocio": ["ocio"],
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
        label="latest",
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
        label="preview",
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

GITHUB_REPO = "AcademySoftwareFoundation/aswf-docker"
MAIN_GITHUB_ASWF_DOCKER_URL = "https://github.com/" + GITHUB_REPO

IMAGE_NAME_REGEX = r"([a-z]+)/ci-(package\-)?([a-z0-9]+):([0-9]+)"
