# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
import logging

from github import Github

from aswfdocker import settings, constants, aswfinfo, groupinfo, utils

logger = logging.getLogger(__name__)


class GitHub:
    def __init__(self):
        s = settings.Settings()
        self.github = Github(s.github_access_token)
        self.repo = self.github.get_repo(constants.GITHUB_REPO)

    def create_release(self, tag, release_message, prerelease):
        logger.debug("GitHub.create_release(tag=%s)", tag)
        self.repo.create_git_tag_and_release(
            tag.replace(":", "/"),
            tag_message="",
            release_name=tag,
            release_message=release_message,
            object=utils.get_current_sha(),
            type="commit",
            draft=False,
            prerelease=prerelease,
        )


class Releaser:
    """Releaser creates GitHub releases for each docker image.
    """

    def __init__(
        self, build_info: aswfinfo.ASWFInfo, group_info: groupinfo.GroupInfo,
    ):
        self.build_info = build_info
        self.group_info = group_info
        self.gh = GitHub()

    def get_message(self):
        return "Inspect released docker image here: https://hub.docker.com/r/aswf/ci-openvdb/tags?page=1&name=2019.4"

    def release(self, dry_run=True):
        logger.debug("Releaser.release(dry_run=%s)", dry_run)
        for image, version in self.group_info.iter_images_versions():
            tag = f"{self.build_info.docker_org}/{image}:{version}"
            prerelease = self.build_info.docker_org == constants.TESTING_DOCKER_ORG
            if dry_run:
                logger.info(
                    "Would create this GitHub release on current commit: %s", tag
                )
            else:
                self.gh.create_release(tag, release_message="", prerelease=prerelease)
