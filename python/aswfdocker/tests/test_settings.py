# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for user settings
"""

import unittest
import tempfile
import os
import logging

from click.testing import CliRunner

from aswfdocker import settings
from aswfdocker.cli import aswfdocker


class TestSettingsCli(unittest.TestCase):
    def setUp(self):
        self._log_handlers = logging.getLogger("").handlers
        logging.getLogger("").handlers = []

    def tearDown(self):
        logging.getLogger("").handlers = self._log_handlers

    def test_settings_cli(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdirname:
            settings_path = os.path.join(tmpdirname, "tmpsettings.yaml")
            result = runner.invoke(
                aswfdocker.cli,
                [
                    "settings",
                    "--github-access-token",
                    "foobar",
                    "--settings-path",
                    settings_path,
                ],
            )
            self.assertEqual(result.output, "")
            self.assertEqual(result.exit_code, 0)
            s = settings.Settings(settings_path=settings_path)
            self.assertEqual(s.github_access_token, "foobar")
