# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
import logging
import typing
from datetime import datetime, timezone

from github import Github, InputGitAuthor

from aswfdocker import settings, constants, aswfinfo, groupinfo

logger = logging.getLogger(__name__)


class GitHub:
    def __init__(self, github_org: str):
        s = settings.Settings()
        if s.github_access_token:
            self.github = Github(s.github_access_token)
        else:
            self.github = Github()
        if not github_org:
            github_org = constants.MAIN_GITHUB_ASWF_ORG
        self.repo = self.github.get_repo(
            f"{github_org}/{constants.MAIN_GITHUB_REPO_NAME}"
        )

    def create_release(self, sha, tag, release_message, prerelease):
        logger.debug("GitHub.create_release(tag=%s)", tag)
        self.repo.create_git_tag_and_release(
            tag=tag.replace(":", "/"),
            tag_message=tag,
            release_name=tag,
            release_message=release_message,
            object=sha,
            type="commit",
            draft=False,
            prerelease=prerelease,
            tagger=InputGitAuthor(
                self.github.get_user().name,
                self.github.get_user().email,
                datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            ),
        )


class Releaser:
    """Releaser creates GitHub releases for each docker image.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        build_info: aswfinfo.ASWFInfo,
        group_info: groupinfo.GroupInfo,
        sha: str,
        github_org="",
        message="",
    ):
        self.github_org = github_org
        self.build_info = build_info
        self.group_info = group_info
        self.sha = sha
        self.message = message
        self.gh = GitHub(github_org)
        self.release_list: typing.List[typing.Tuple[str]] = []

    def gather(self):
        for image, version in self.group_info.iter_images_versions():
            tag = f"{self.build_info.docker_org}/{image}:{version}"
            self.release_list.append((image, version, tag))

    def release(self, dry_run=True):
        logger.debug("Releaser.release(dry_run=%s)", dry_run)
        prerelease = self.build_info.docker_org == constants.TESTING_DOCKER_ORG
        if self.message:
            start_message = f"{self.message}\n\n"
        else:
            start_message = self.message
        for image, version, tag in self.release_list:
            message = (
                f"{start_message}Inspect released docker image here: "
                f"https://hub.docker.com/r/{self.build_info.docker_org}/{image}/tags?name={version}"
            )
            if dry_run:
                logger.info(
                    "Would create this GitHub release on current commit: %s", tag
                )
            else:
                self.gh.create_release(
                    self.sha, tag, release_message=message, prerelease=prerelease
                )
