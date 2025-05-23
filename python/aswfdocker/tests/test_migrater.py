# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for the migrate command
"""
import unittest
import logging

from click.testing import CliRunner

from aswfdocker import migrater, index, constants
from aswfdocker.cli import aswfdocker


class TestMigrater(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_migrate_nofilter(self):
        m = migrater.Migrater("src", "dst")
        m.gather("", "")
        self.assertGreater(len(m.migration_list), 10)

    def test_migrate_pkgfilter(self):
        m = migrater.Migrater("src", "dst")
        m.gather("openexr", "")
        self.assertEqual(len(m.migration_list), 7)

    def test_migrate_versionfilter(self):
        m = migrater.Migrater("src", "dst")
        m.gather("openexr", "2019")
        current_version = list(
            index.Index().iter_versions(constants.ImageType.PACKAGE, "openexr")
        )[0]
        self.assertEqual(len(m.migration_list), 1)
        minfo = m.migration_list[0]
        self.assertEqual(minfo.image, "ci-package-openexr")
        oexr_version = list(
            index.Index().iter_versions(constants.ImageType.PACKAGE, "openexr")
        )[0]
        self.assertEqual(minfo.version, oexr_version)
        self.assertEqual(
            minfo.source,
            f"{constants.DOCKER_REGISTRY}/src/ci-package-openexr:{current_version}",
        )
        self.assertEqual(
            minfo.destination,
            f"{constants.DOCKER_REGISTRY}/dst/ci-package-openexr:{current_version}",
        )

        m.migrate(dry_run=True)
        reg = constants.DOCKER_REGISTRY
        self.assertEqual(
            m.cmds,
            [
                f"docker pull {reg}/src/ci-package-openexr:{current_version}",
                f"docker tag {reg}/src/ci-package-openexr:{current_version} "
                f"{reg}/dst/ci-package-openexr:{current_version}",
                f"docker push {reg}/dst/ci-package-openexr:{current_version}",
                f"docker tag {reg}/dst/ci-package-openexr:{current_version} "
                f"{reg}/dst/ci-package-openexr:2019",
                f"docker push {reg}/dst/ci-package-openexr:2019",
            ],
        )


class TestMigraterCli(unittest.TestCase):
    def setUp(self):
        self._log_handlers = logging.getLogger("").handlers
        logging.getLogger("").handlers = []

    def tearDown(self):
        logging.getLogger("").handlers = self._log_handlers

    def test_migrate_cli(self):
        runner = CliRunner()
        result = runner.invoke(
            aswfdocker.cli,
            [
                "migrate",
                "--from",
                "src",
                "--to",
                "dst",
                "--package",
                "openexr",
                "--version",
                "2019",
                "--dry-run",
            ],
            input="y\n",
        )
        self.assertEqual(result.exit_code, 0)
        current_version = list(
            index.Index().iter_versions(constants.ImageType.PACKAGE, "openexr")
        )[0]
        reg = constants.DOCKER_REGISTRY
        self.assertEqual(
            result.output,
            f"Are you sure you want to migrate the following 1 packages?\n"
            f"{reg}/src/ci-package-openexr:{current_version} -> "
            f"{reg}/dst/ci-package-openexr:{current_version}\n"
            f" [y/N]: y\n"
            f"INFO:aswfdocker.migrater:Migrating "
            f"{reg}/src/ci-package-openexr:{current_version} -> "
            f"{reg}/dst/ci-package-openexr:{current_version}\n"
            f"Migration done.\n",
        )
