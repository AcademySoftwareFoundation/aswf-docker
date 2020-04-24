# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for the build command
"""

import unittest
import logging
import tempfile

from click.testing import CliRunner

from aswfdocker import builder, aswfinfo, constants
from aswfdocker.cli import aswfdocker


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.build_info = aswfinfo.ASWFInfo(
            repo_uri="notauri", source_branch="testing", aswf_version="2019.123"
        )

    def test_package_baseqt_2019_dict(self):
        b = builder.Builder(
            self.build_info,
            builder.GroupInfo(
                names=["baseqt"], versions=["2019"], type_=constants.ImageType.PACKAGE,
            ),
        )
        self.assertEqual(
            b.make_bake_dict(),
            {
                "group": {"default": {"targets": ["package-qt"]}},
                "target": {
                    "package-qt": {
                        "context": ".",
                        "dockerfile": "packages/Dockerfile",
                        "args": {
                            "ASWF_ORG": "aswflocaltesting",
                            "ASWF_PKG_ORG": "aswftesting",
                            "ASWF_VERSION": constants.VERSIONS[
                                constants.ImageType.PACKAGE
                            ]["qt"][1],
                            "BUILD_DATE": constants.DEV_BUILD_DATE,
                            "CI_COMMON_VERSION": "1",
                            "PYTHON_VERSION": "2.7",
                            "VCS_REF": constants.DEV_BUILD_DATE,
                            "VFXPLATFORM_VERSION": "2019",
                        },
                        "tags": [
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-package-qt:2019",
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-package-qt:{constants.VERSIONS[constants.ImageType.PACKAGE]['qt'][1]}",
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-package-qt:latest",
                        ],
                        "target": "ci-qt-package",
                        "output": ["type=docker"],
                    }
                },
            },
        )

    def test_image_base_2019_dict(self):
        b = builder.Builder(
            self.build_info,
            builder.GroupInfo(
                names=["base"], versions=["2019"], type_=constants.ImageType.IMAGE,
            ),
        )
        self.assertEqual(
            b.make_bake_dict(),
            {
                "group": {"default": {"targets": ["image-base"]}},
                "target": {
                    "image-base": {
                        "context": ".",
                        "dockerfile": "ci-base/Dockerfile",
                        "args": {
                            "ASWF_ORG": "aswflocaltesting",
                            "ASWF_PKG_ORG": "aswftesting",
                            "ASWF_VERSION": constants.VERSIONS[
                                constants.ImageType.IMAGE
                            ]["base"][1],
                            "BUILD_DATE": constants.DEV_BUILD_DATE,
                            "CI_COMMON_VERSION": "1",
                            "PYTHON_VERSION": "2.7",
                            "VCS_REF": constants.DEV_BUILD_DATE,
                            "VFXPLATFORM_VERSION": "2019",
                        },
                        "tags": [
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:2019",
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:{constants.VERSIONS[constants.ImageType.IMAGE]['base'][1]}",
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:latest",
                        ],
                        "output": ["type=docker"],
                    }
                },
            },
        )


class TestBuilderCli(unittest.TestCase):
    def setUp(self):
        logging.getLogger("").handlers = []

    def test_builder_cli(self):
        runner = CliRunner()
        result = runner.invoke(
            aswfdocker.cli,
            [
                "build",
                "--ci-image-type",
                "PACKAGE",
                "--group-name",
                "vfx",
                "--group-version",
                "2019",
                "--target",
                "openexr",
                "--dry-run",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output,
            f"INFO:aswfdocker.builder:Would build: 'docker buildx bake -f {tempfile.gettempdir()}/docker-bake-PACKAGE-vfx-2019.json --progress auto'\n",
        )

    def test_builderlist_cli(self):
        runner = CliRunner()
        result = runner.invoke(
            aswfdocker.cli,
            [
                "build",
                "--ci-image-type",
                "PACKAGE",
                "--group-name",
                "vfx",
                "--group-version",
                "2019,2020",
                "--target",
                "openexr",
                "--dry-run",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output,
            f"INFO:aswfdocker.builder:Would build: 'docker buildx bake -f {tempfile.gettempdir()}/docker-bake-PACKAGE-vfx-2019-2020.json --progress auto'\n",
        )
