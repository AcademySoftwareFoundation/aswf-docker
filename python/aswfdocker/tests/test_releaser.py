# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0


import unittest
from unittest import mock
import logging
import tempfile

from click.testing import CliRunner

from aswfdocker import releaser, aswfinfo, index, constants, groupinfo, utils
from aswfdocker.cli import aswfdocker


class TestReleaser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.build_info = aswfinfo.ASWFInfo(
            repo_uri="notauri", source_branch="testing", aswf_version="2019.123"
        )

    def test_package_baseqt_2019_dict(self):
        r = releaser.Releaser(
            self.build_info,
            groupinfo.GroupInfo(
                names=["base"],
                versions=["2019"],
                type_=constants.ImageType.PACKAGE,
                target="boost",
            ),
        )
        r.gh.repo.create_git_tag_and_release = mock.MagicMock()
        r.release(dry_run=False)
        boost_version = list(
            index.Index().iter_versions(constants.ImageType.PACKAGE, "boost")
        )[1]
        r.gh.repo.create_git_tag_and_release.assert_called_with(
            "aswflocaltesting/ci-package-boost/2019.1",
            draft=False,
            object=utils.get_current_sha(),
            prerelease=False,
            release_message=f"Inspect released docker image here: https://hub.docker.com/r/aswflocaltesting/ci-package-boost/tags?name={boost_version}",
            release_name=f"aswflocaltesting/ci-package-boost:{boost_version}",
            tag_message="",
            type="commit",
        )
