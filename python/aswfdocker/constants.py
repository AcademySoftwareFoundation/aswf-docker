# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Main configuration and constants for aswfdocker
"""
import enum


class ImageType(enum.Enum):
    IMAGE = "image"
    PACKAGE = "package"


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

IMAGE_NAME_REGEX = r"(refs/tags/)?(?P<org>[a-z]+)/ci-(?P<package>package\-)?(?P<image>[a-z0-9]+)[:/](?P<version>[0-9\.a-z\-]+)"
