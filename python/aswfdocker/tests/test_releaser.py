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
                names=["baseqt"], versions=["2019"], type_=constants.ImageType.PACKAGE,
            ),
        )
        r.gh.repo.create_git_tag_and_release = mock.MagicMock()
        r.release(dry_run=False)
        r.gh.repo.create_git_tag_and_release.assert_called_with(
            "aswflocaltesting/qt/2019.1",
            draft=False,
            object=utils.get_current_sha(),
            prerelease=False,
            release_message="",
            release_name="aswflocaltesting/qt:2019.1",
            tag_message="",
            type="commit",
        )
