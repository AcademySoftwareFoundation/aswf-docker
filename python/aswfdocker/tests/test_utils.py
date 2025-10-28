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

from aswfdocker import utils, index, constants
from aswfdocker.cli import aswfdocker


class TestUtils(unittest.TestCase):
    def test_get_docker_org(self):
        self.assertEqual(utils.get_docker_org("", ""), "aswftesting")
        self.assertEqual(
            utils.get_docker_org(
                constants.MAIN_GITHUB_ASWF_DOCKER_URL,
                "refs/heads/main",
            ),
            "aswf",
        )
        self.assertEqual(
            utils.get_docker_org(
                constants.MAIN_GITHUB_ASWF_DOCKER_URL,
                "refs/heads/testing",
            ),
            "aswftesting",
        )
        self.assertEqual(
            utils.get_docker_org(
                "https://github.com/randomfork/aswf-docker", "refs/heads/main"
            ),
            "aswflocaltesting",
        )
        self.assertEqual(
            utils.get_docker_org(
                "https://github.com/randomfork/aswf-docker", "refs/heads/randombranch"
            ),
            "aswflocaltesting",
        )

    def test_get_docker_push(self):
        self.assertFalse(utils.get_docker_push("", ""))
        self.assertTrue(
            utils.get_docker_push(
                constants.MAIN_GITHUB_ASWF_DOCKER_URL,
                "refs/heads/main",
            )
        )
        self.assertTrue(
            utils.get_docker_push(
                constants.MAIN_GITHUB_ASWF_DOCKER_URL,
                "refs/heads/testing",
            )
        )
        self.assertFalse(
            utils.get_docker_push(
                "https://github.com/randomfork/aswf-docker", "refs/heads/main"
            )
        )
        self.assertFalse(
            utils.get_docker_push(
                "https://github.com/randomfork/aswf-docker", "refs/heads/randombranch"
            )
        )

    def test_image_def_from_name(self):
        with self.assertRaises(RuntimeError):
            utils.get_image_spec("aswf/ci-package-openvdb_2018")
        self.assertEqual(
            utils.get_image_spec("aswftesting/ci-common:1"),
            ("aswftesting", constants.ImageType.IMAGE, "common", "1"),
        )
        self.assertEqual(
            utils.get_image_spec("aswf/ci-package-openvdb:2018"),
            ("aswf", constants.ImageType.PACKAGE, "openvdb", "2018"),
        )
        self.assertEqual(
            utils.get_image_spec("refs/tags/aswf/ci-package-openvdb/2018"),
            ("aswf", constants.ImageType.PACKAGE, "openvdb", "2018"),
        )
        self.assertEqual(
            utils.get_image_spec("aswf/ci-package-clang:1-clang6"),
            ("aswf", constants.ImageType.PACKAGE, "clang", "1-clang6"),
        )


class TestUtilsCli(unittest.TestCase):
    def setUp(self):
        self._log_handlers = logging.getLogger("").handlers
        logging.getLogger("").handlers = []
        self.maxDiff = None

    def tearDown(self):
        logging.getLogger("").handlers = self._log_handlers

    def test_cli_getdockerorg(self):
        runner = CliRunner()
        result = runner.invoke(aswfdocker.cli, ["getdockerorg"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "aswftesting")

    def test_cli_getdockerorgforced(self):
        runner = CliRunner()
        result = runner.invoke(
            aswfdocker.cli,
            [
                "--repo-uri",
                "https://github.com/AcademySoftwareFoundation/aswf-docker",
                "--source-branch",
                "refs/heads/main",
                "getdockerorg",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "aswf")

    def test_cli_getdockerpush(self):
        runner = CliRunner()
        result = runner.invoke(aswfdocker.cli, ["getdockerpush"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "false")

    def test_cli_download(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdirname:
            result = runner.invoke(
                aswfdocker.cli,
                [
                    "--repo-root",
                    tmpdirname,
                    "download",
                    "--package",
                    "tbb",
                    "--version",
                    "2019",
                ],
                catch_exceptions=False,
            )
            self.assertEqual(result.exit_code, 0)
            path = os.path.join(tmpdirname, "packages", "2019", "tbb.tar.gz")
            self.assertEqual(result.output, path)
            self.assertTrue(os.path.exists(result.output))

    def test_cli_packages(self):
        runner = CliRunner()
        result = runner.invoke(aswfdocker.cli, ["packages"], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        pkgs = result.output.split("\n")
        self.assertGreater(len(pkgs), 20)
        clang_version = list(
            index.Index().iter_versions(constants.ImageType.PACKAGE, "clang")
        )[0]
        self.assertEqual(
            pkgs[0],
            f"common/ci-package-clang:{clang_version}",
        )

    def test_cli_images(self):
        runner = CliRunner()
        result = runner.invoke(aswfdocker.cli, ["images"], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        imgs = result.output.split("\n")
        self.assertGreater(len(imgs), 15)
        baseos_gl_conan_version = list(
            index.Index().iter_versions(constants.ImageType.IMAGE, "baseos-gl-conan")
        )[0]
        self.assertEqual(
            imgs[0],
            f"baseos-gl-conan/ci-baseos-gl-conan:{baseos_gl_conan_version}",
        )
