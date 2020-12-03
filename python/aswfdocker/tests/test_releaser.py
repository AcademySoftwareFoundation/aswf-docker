# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0


import unittest
from unittest import mock
import logging
import tempfile

from github import InputGitAuthor

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
                names=["base1"],
                versions=["2019"],
                type_=constants.ImageType.PACKAGE,
                targets=["boost"],
            ),
            sha=utils.get_current_sha(),
        )
        r.gh.repo.create_git_tag_and_release = mock.MagicMock()

        class u:
            name = "testuser"
            email = "testuser@test.user"

        r.gh.github.get_user = mock.MagicMock(return_value=u())

        r.gather()
        r.release(dry_run=False)
        boost_version = list(
            index.Index().iter_versions(constants.ImageType.PACKAGE, "boost")
        )[1]
        r.gh.repo.create_git_tag_and_release.assert_called_once_with(
            tag=f"aswflocaltesting/ci-package-boost/{boost_version}",
            draft=False,
            object=utils.get_current_sha(),
            prerelease=False,
            release_message=f"Inspect released Docker image here: https://hub.docker.com/r/aswflocaltesting/ci-package-boost/tags?name={boost_version}",
            release_name=f"aswflocaltesting/ci-package-boost:{boost_version}",
            tag_message=f"aswflocaltesting/ci-package-boost:{boost_version}",
            type="commit",
            tagger=mock.ANY,
        )


class TestReleaserCli(unittest.TestCase):
    def setUp(self):
        self._log_handlers = logging.getLogger("").handlers
        logging.getLogger("").handlers = []
        self.maxDiff = None

    def tearDown(self):
        logging.getLogger("").handlers = self._log_handlers

    def test_migrate_cli(self):
        current_version = list(
            index.Index().iter_versions(constants.ImageType.PACKAGE, "boost")
        )[1]
        runner = CliRunner()
        result = runner.invoke(
            aswfdocker.cli,
            [
                "release",
                "-n",
                f"aswf/ci-package-boost:{current_version}",
                "--sha",
                utils.get_current_sha(),
                "--dry-run",
            ],
            input="y\n",
        )
        self.assertFalse(result.exception)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output,
            f"""Are you sure you want to create the following 1 release on sha={utils.get_current_sha()}?
aswf/ci-package-boost:{current_version}
 [y/N]: y
INFO:aswfdocker.releaser:Would create this GitHub release on current commit: aswf/ci-package-boost:{current_version}
Release done.
""",
        )
