# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for the utility commands
"""

import unittest
import logging
import tempfile
import os

from click.testing import CliRunner

from aswfdocker import utils, index, constants, dockergen
from aswfdocker.cli import aswfdocker


class TestDockerGen(unittest.TestCase):
    def test_dockergen(self):
        dg = dockergen.DockerGen("base")
        self.assertTrue(dg.check_dockerfile())
        self.assertTrue(dg.check_readme())


class TestUtilsCli(unittest.TestCase):
    def setUp(self):
        self._log_handlers = logging.getLogger("").handlers
        logging.getLogger("").handlers = []
        self.maxDiff = None

    def tearDown(self):
        logging.getLogger("").handlers = self._log_handlers

    def test_cli_dockergen(self):
        runner = CliRunner()
        result = runner.invoke(aswfdocker.cli, ["dockergen", "--check", "-n", "base"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output,
            "/home/ggaloys/dev/aswf-docker/ci-base/Dockerfile is up to date\n"
            "/home/ggaloys/dev/aswf-docker/ci-base/README.md is up to date\n",
        )
