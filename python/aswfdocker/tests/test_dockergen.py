# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for the utility commands
"""

import unittest
import logging

from click.testing import CliRunner

from aswfdocker import dockergen
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
        self.assertEqual(result.exit_code, 0, msg=f"output: {result.output}")
        lines = result.output.split("\n")
        # First two lines are for the requested image; subsequent lines are
        # for Conan profiles (always checked regardless of --image-name).
        self.assertTrue(lines[0].endswith("ci-base/Dockerfile is up to date"))
        self.assertTrue(lines[1].endswith("ci-base/README.md is up to date"))
        self.assertTrue(
            any("ci_common" in line and "profiles" in line for line in lines),
            "Expected Conan ci_common profile check lines in output",
        )
        self.assertTrue(
            any("vfx" in line and "profiles" in line for line in lines),
            "Expected Conan vfx profile check lines in output",
        )


class TestConanProfileZlibInCommon(unittest.TestCase):
    def test_ci_common_profile_pins_zlib(self):
        gen = dockergen.ConanProfileGen("7")
        path, content = gen._render()  # pylint: disable=protected-access
        self.assertTrue(path.endswith("ci_common7"))
        self.assertIn("zlib/*: zlib/", content)
        self.assertIn("@{{ org }}/ci_common7", content)

    def test_vfx_profile_inherits_zlib_from_ci_common(self):
        gen = dockergen.ConanProfileGen("2026")
        path, content = gen._render()  # pylint: disable=protected-access
        self.assertTrue(path.endswith("vfx2026"))
        self.assertIn("include(ci_common6)", content)
        # zlib is defined in ci_common (included), not re-pinned to the vfx channel
        self.assertNotIn("zlib/*:", content)


class TestCMakeZlibDependency(unittest.TestCase):
    def test_cmake_recipe_requires_conan_zlib(self):
        from pathlib import Path

        conanfile = (
            Path(__file__).resolve().parents[3]
            / "packages"
            / "conan"
            / "recipes"
            / "cmake"
            / "conanfile.py"
        )
        text = conanfile.read_text(encoding="utf-8")
        self.assertIn('self.requires("zlib/[>=1.2.11 <2]")', text)
        self.assertIn('CMAKE_USE_SYSTEM_ZLIB"] = True', text)
        self.assertNotIn("breaks dependency order", text)
