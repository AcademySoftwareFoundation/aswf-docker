# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
ASWF repository information
"""
from aswfdocker import utils, constants


class ASWFInfo:
    """Information about the current state of the ASWF repository
    """

    def __init__(
        self,
        repo_uri: str = "",
        source_branch: str = "",
        aswf_version: str = "",
        repo_root: str = "",
    ):
        self.aswf_version = aswf_version
        self.repo_uri = repo_uri
        self.source_branch = source_branch
        self.docker_org = utils.get_docker_org(repo_uri, source_branch)
        self.repo_root = repo_root
        if self.docker_org == constants.FAKE_DOCKER_ORG:
            self.package_org = constants.TESTING_DOCKER_ORG
        else:
            self.package_org = self.docker_org
        if self.docker_org == constants.PUBLISH_DOCKER_ORG:
            self.vcs_ref = utils.get_current_sha()
            self.build_date = utils.get_current_date()
        else:
            self.vcs_ref = constants.DEV_BUILD_DATE
            self.build_date = constants.DEV_BUILD_DATE

    def set_org(self, org):
        self.docker_org = org
        self.package_org = org
