# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for the build command
"""

import unittest
import logging
import tempfile

from click.testing import CliRunner

from aswfdocker import builder, aswfinfo, index, constants, groupinfo
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
            groupinfo.GroupInfo(
                names=["base2"],
                versions=["2019"],
                type_=constants.ImageType.PACKAGE,
                targets=[],
            ),
        )
        qt_version = list(
            index.Index().iter_versions(constants.ImageType.PACKAGE, "qt")
        )[1]
        baked = b.make_bake_dict()
        self.assertEqual(
            baked["target"]["ci-package-qt-2019"]["tags"],
            [
                f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-package-qt:2019",
                f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-package-qt:{qt_version}",
                f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-package-qt:latest",
                f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-package-qt:2019-5.12.6",
            ],
        )
        self.assertEqual(
            baked["target"]["ci-package-qt-2019"]["args"]["ASWF_VERSION"], qt_version
        )
        self.assertEqual(
            baked["target"]["ci-package-qt-2019"]["dockerfile"],
            "packages/base2/Dockerfile",
        )

    def test_image_base_2019_dict(self):
        b = builder.Builder(
            self.build_info,
            groupinfo.GroupInfo(
                names=["base"],
                versions=["2019"],
                type_=constants.ImageType.IMAGE,
                targets=[],
            ),
        )
        base_version = list(
            index.Index().iter_versions(constants.ImageType.IMAGE, "base")
        )[1]
        baked = b.make_bake_dict()
        self.assertEqual(
            baked["target"]["ci-base-2019"]["tags"],
            [
                f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:2019",
                f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:{base_version}",
                f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:latest",
            ],
        )
        self.assertEqual(
            baked["target"]["ci-base-2019"]["args"]["ASWF_VERSION"], base_version
        )

    def test_image_base_2019clang_dict(self):
        b = builder.Builder(
            self.build_info,
            groupinfo.GroupInfo(
                names=["vfx3"],
                versions=["2019-clang9"],
                type_=constants.ImageType.IMAGE,
                targets=["openvdb"],
            ),
        )
        openvdb_version = list(
            index.Index().iter_versions(constants.ImageType.IMAGE, "openvdb")
        )[4]
        self.assertEqual(
            b.make_bake_dict(),
            {
                "group": {"default": {"targets": ["ci-openvdb-2019-clang9"]}},
                "target": {
                    "ci-openvdb-2019-clang9": {
                        "context": ".",
                        "dockerfile": "ci-openvdb/Dockerfile",
                        "args": {
                            "ASWF_ALEMBIC_VERSION": "1.7.11",
                            "ASWF_ORG": "aswflocaltesting",
                            "ASWF_PKG_ORG": "aswftesting",
                            "ASWF_VERSION": openvdb_version,
                            "ASWF_BLOSC_VERSION": "1.5.0",
                            "ASWF_BOOST_VERSION": "1.66.0",
                            "ASWF_CCACHE_VERSION": "4.0",
                            "CI_COMMON_VERSION": "1",
                            "ASWF_CLANG_MAJOR_VERSION": "9",
                            "ASWF_CLANG_VERSION": "9.0.1",
                            "ASWF_CMAKE_VERSION": "3.12.4",
                            "ASWF_CPPUNIT_VERSION": "1.14.0",
                            "ASWF_CUDA_VERSION": "10.2",
                            "ASWF_DTS_VERSION": "6",
                            "ASWF_GLEW_VERSION": "2.1.0",
                            "ASWF_GLFW_VERSION": "3.1.2",
                            "ASWF_HDF5_VERSION": "1.8.21",
                            "ASWF_LOG4CPLUS_VERSION": "1.1.2",
                            "ASWF_NINJA_VERSION": "1.10.1",
                            "ASWF_NUMPY_VERSION": "1.14",
                            "ASWF_OCIO_CONFIGS_VERSION": "1.0_r2",
                            "ASWF_OCIO_VERSION": "1.1.0",
                            "ASWF_OIIO_VERSION": "2.0.8",
                            "ASWF_OPENEXR_VERSION": "2.3.0",
                            "ASWF_OPENSUBDIV_VERSION": "3_3_3",
                            "ASWF_OPENVDB_VERSION": "6.2.1",
                            "ASWF_OSL_VERSION": "1.10.9",
                            "ASWF_OTIO_VERSION": "0.12.1",
                            "ASWF_PARTIO_VERSION": "1.10.1",
                            "ASWF_PTEX_VERSION": "2.1.33",
                            "ASWF_PYBIND11_VERSION": "2.6.2",
                            "ASWF_PYSIDE_VERSION": "5.12.6",
                            "ASWF_PYTHON_VERSION": "2.7.15",
                            "ASWF_PYTHON_MAJOR_MINOR_VERSION": "2.7",
                            "ASWF_QT_VERSION": "5.12.6",
                            "ASWF_SONAR_VERSION": "4.5.0.2216",
                            "ASWF_TBB_VERSION": "2018",
                            "ASWF_USD_VERSION": "19.11",
                            "ASWF_VFXPLATFORM_VERSION": "2019",
                        },
                        "labels": {
                            "org.opencontainers.image.created": constants.DEV_BUILD_DATE,
                            "org.opencontainers.image.revision": constants.DEV_BUILD_DATE,
                        },
                        "tags": [
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-openvdb:2019-clang9",
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-openvdb:{openvdb_version}",
                        ],
                        "output": ["type=docker"],
                    }
                },
            },
        )

    def test_image_base_2019_2020_dict(self):
        b = builder.Builder(
            self.build_info,
            groupinfo.GroupInfo(
                names=["base"],
                versions=["2019", "2020"],
                type_=constants.ImageType.IMAGE,
                targets=["base"],
            ),
        )
        base_versions = list(
            index.Index().iter_versions(constants.ImageType.IMAGE, "base")
        )
        self.assertEqual(
            b.make_bake_dict(),
            {
                "group": {"default": {"targets": ["ci-base-2019", "ci-base-2020"]}},
                "target": {
                    "ci-base-2020": {
                        "context": ".",
                        "dockerfile": "ci-base/Dockerfile",
                        "args": {
                            "ASWF_ALEMBIC_VERSION": "1.7.12",
                            "ASWF_ORG": "aswflocaltesting",
                            "ASWF_PKG_ORG": "aswftesting",
                            "ASWF_VERSION": base_versions[2],
                            "ASWF_BLOSC_VERSION": "1.5.0",
                            "ASWF_BOOST_VERSION": "1.70.0",
                            "ASWF_CCACHE_VERSION": "4.0",
                            "CI_COMMON_VERSION": "1",
                            "ASWF_CLANG_MAJOR_VERSION": "7",
                            "ASWF_CLANG_VERSION": "7.1.0",
                            "ASWF_CMAKE_VERSION": "3.18.4",
                            "ASWF_CPPUNIT_VERSION": "1.15.1",
                            "ASWF_CUDA_VERSION": "10.2",
                            "ASWF_DTS_VERSION": "6",
                            "ASWF_GLEW_VERSION": "2.1.0",
                            "ASWF_GLFW_VERSION": "3.1.2",
                            "ASWF_HDF5_VERSION": "1.8.21",
                            "ASWF_LOG4CPLUS_VERSION": "1.1.2",
                            "ASWF_NINJA_VERSION": "1.10.1",
                            "ASWF_NUMPY_VERSION": "1.16",
                            "ASWF_OCIO_CONFIGS_VERSION": "1.0_r2",
                            "ASWF_OCIO_VERSION": "1.1.1",
                            "ASWF_OIIO_VERSION": "2.1.13.0",
                            "ASWF_OPENEXR_VERSION": "2.4.0",
                            "ASWF_OPENSUBDIV_VERSION": "3_4_3",
                            "ASWF_OPENVDB_VERSION": "7.1.0",
                            "ASWF_OSL_VERSION": "1.10.10",
                            "ASWF_OTIO_VERSION": "0.12.1",
                            "ASWF_PARTIO_VERSION": "1.10.1",
                            "ASWF_PTEX_VERSION": "2.3.2",
                            "ASWF_PYBIND11_VERSION": "2.6.2",
                            "ASWF_PYSIDE_VERSION": "5.12.6",
                            "ASWF_PYTHON_VERSION": "3.7.3",
                            "ASWF_PYTHON_MAJOR_MINOR_VERSION": "3.7",
                            "ASWF_QT_VERSION": "5.12.6",
                            "ASWF_SONAR_VERSION": "4.5.0.2216",
                            "ASWF_TBB_VERSION": "2019_U6",
                            "ASWF_USD_VERSION": "20.11",
                            "ASWF_VFXPLATFORM_VERSION": "2020",
                        },
                        "labels": {
                            "org.opencontainers.image.created": constants.DEV_BUILD_DATE,
                            "org.opencontainers.image.revision": constants.DEV_BUILD_DATE,
                        },
                        "tags": [
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:2020",
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:{base_versions[2]}",
                        ],
                        "output": ["type=docker"],
                    },
                    "ci-base-2019": {
                        "context": ".",
                        "dockerfile": "ci-base/Dockerfile",
                        "args": {
                            "ASWF_ALEMBIC_VERSION": "1.7.11",
                            "ASWF_ORG": "aswflocaltesting",
                            "ASWF_PKG_ORG": "aswftesting",
                            "ASWF_VERSION": base_versions[1],
                            "ASWF_BLOSC_VERSION": "1.5.0",
                            "ASWF_BOOST_VERSION": "1.66.0",
                            "ASWF_CCACHE_VERSION": "4.0",
                            "CI_COMMON_VERSION": "1",
                            "ASWF_CLANG_MAJOR_VERSION": "7",
                            "ASWF_CLANG_VERSION": "7.1.0",
                            "ASWF_CMAKE_VERSION": "3.12.4",
                            "ASWF_CPPUNIT_VERSION": "1.14.0",
                            "ASWF_CUDA_VERSION": "10.2",
                            "ASWF_DTS_VERSION": "6",
                            "ASWF_GLEW_VERSION": "2.1.0",
                            "ASWF_GLFW_VERSION": "3.1.2",
                            "ASWF_HDF5_VERSION": "1.8.21",
                            "ASWF_LOG4CPLUS_VERSION": "1.1.2",
                            "ASWF_NINJA_VERSION": "1.10.1",
                            "ASWF_NUMPY_VERSION": "1.14",
                            "ASWF_OCIO_CONFIGS_VERSION": "1.0_r2",
                            "ASWF_OCIO_VERSION": "1.1.0",
                            "ASWF_OIIO_VERSION": "2.0.8",
                            "ASWF_OPENEXR_VERSION": "2.3.0",
                            "ASWF_OPENSUBDIV_VERSION": "3_3_3",
                            "ASWF_OPENVDB_VERSION": "6.2.1",
                            "ASWF_OSL_VERSION": "1.10.9",
                            "ASWF_OTIO_VERSION": "0.12.1",
                            "ASWF_PARTIO_VERSION": "1.10.1",
                            "ASWF_PTEX_VERSION": "2.1.33",
                            "ASWF_PYBIND11_VERSION": "2.6.2",
                            "ASWF_PYSIDE_VERSION": "5.12.6",
                            "ASWF_PYTHON_VERSION": "2.7.15",
                            "ASWF_PYTHON_MAJOR_MINOR_VERSION": "2.7",
                            "ASWF_QT_VERSION": "5.12.6",
                            "ASWF_SONAR_VERSION": "4.5.0.2216",
                            "ASWF_TBB_VERSION": "2018",
                            "ASWF_USD_VERSION": "19.11",
                            "ASWF_VFXPLATFORM_VERSION": "2019",
                        },
                        "labels": {
                            "org.opencontainers.image.created": constants.DEV_BUILD_DATE,
                            "org.opencontainers.image.revision": constants.DEV_BUILD_DATE,
                        },
                        "tags": [
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:2019",
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:{base_versions[1]}",
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:latest",
                        ],
                        "output": ["type=docker"],
                    },
                },
            },
        )


class TestBuilderCli(unittest.TestCase):
    def setUp(self):
        self._log_handlers = logging.getLogger("").handlers
        logging.getLogger("").handlers = []

    def tearDown(self):
        logging.getLogger("").handlers = self._log_handlers

    def test_builder_cli(self):
        runner = CliRunner()
        result = runner.invoke(
            aswfdocker.cli,
            [
                "build",
                "--ci-image-type",
                "PACKAGE",
                "--version",
                "2019",
                "--target",
                "openexr",
                "--dry-run",
            ],
        )
        self.assertFalse(result.exception)
        self.assertEqual(
            result.output,
            f"INFO:aswfdocker.builder:Would build: 'docker buildx bake -f {tempfile.gettempdir()}/docker-bake-PACKAGE-vfx1-2019.json --progress auto'\n",
        )
        self.assertEqual(result.exit_code, 0)

    def test_builder_cli_fromtag(self):
        runner = CliRunner()
        result = runner.invoke(
            aswfdocker.cli,
            ["build", "--full-name", "aswftesting/ci-common:1", "--dry-run",],
        )
        self.assertFalse(result.exception)
        self.assertEqual(
            result.output,
            f"INFO:aswfdocker.builder:Would build: 'docker buildx bake -f {tempfile.gettempdir()}/docker-bake-IMAGE-common-1.json --progress auto'\n",
        )
        self.assertEqual(result.exit_code, 0)

    def test_builderlist_cli(self):
        runner = CliRunner()
        result = runner.invoke(
            aswfdocker.cli,
            [
                "build",
                "--ci-image-type",
                "PACKAGE",
                "--version",
                "2019",
                "--version",
                "2020",
                "--target",
                "openexr",
                "--dry-run",
            ],
        )
        self.assertFalse(result.exception)
        self.assertEqual(
            result.output,
            f"INFO:aswfdocker.builder:Would build: 'docker buildx bake -f {tempfile.gettempdir()}/docker-bake-PACKAGE-vfx1-2019-2020.json --progress auto'\n",
        )
        self.assertEqual(result.exit_code, 0)
