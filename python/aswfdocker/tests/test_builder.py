# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for the build command
"""

import os
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
        )[0]
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

    def test_package_baseqt_2019_dict_conan(self):
        b = builder.Builder(
            self.build_info,
            groupinfo.GroupInfo(
                names=["base2"],
                versions=["2019"],
                type_=constants.ImageType.PACKAGE,
                targets=[],
            ),
            use_conan=True,
        )
        baked = b.make_bake_dict()
        self.assertIn("ASWF_QT_VERSION", baked["target"]["ci-package-qt-1"]["args"])
        self.assertEqual(
            baked["target"]["ci-package-qt-1"]["tags"],
            [
                f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-centos7-gl-conan:1",
                f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-centos7-gl-conan:1",
            ],
        )
        self.assertEqual(
            baked["target"]["ci-package-qt-1"]["args"]["ASWF_VERSION"], "1"
        )
        self.assertEqual(
            baked["target"]["ci-package-qt-1"]["dockerfile"],
            "packages/common/Dockerfile",
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
        )[0]
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
        )[3]
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
                            "ASWF_CONAN_CHANNEL": "vfx2019",
                            "ASWF_CONAN_PYTHON_VERSION": "3.9.11",
                            "ASWF_CONAN_VERSION": "1.47.0",
                            "ASWF_CUDA_VERSION": "10.2",
                            "ASWF_DTS_VERSION": "6",
                            "ASWF_GLEW_VERSION": "2.1.0",
                            "ASWF_GLFW_VERSION": "3.1.2",
                            "ASWF_GTEST_VERSION": "1.8.1",
                            "ASWF_HDF5_VERSION": "1.8.21",
                            "ASWF_IMATH_VERSION": "2.3.0",
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
                            "ASWF_PYBIND11_VERSION": "2.4.3",
                            "ASWF_PYSIDE_VERSION": "5.12.6",
                            "ASWF_PYTHON_VERSION": "2.7.15",
                            "ASWF_PYTHON_MAJOR_MINOR_VERSION": "2.7",
                            "ASWF_QT_VERSION": "5.12.6",
                            "ASWF_SONAR_VERSION": "4.6.2.2472",
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
                            "ASWF_VERSION": base_versions[1],
                            "ASWF_BLOSC_VERSION": "1.5.0",
                            "ASWF_BOOST_VERSION": "1.70.0",
                            "ASWF_CCACHE_VERSION": "4.0",
                            "CI_COMMON_VERSION": "1",
                            "ASWF_CLANG_MAJOR_VERSION": "7",
                            "ASWF_CLANG_VERSION": "7.1.0",
                            "ASWF_CMAKE_VERSION": "3.18.4",
                            "ASWF_CPPUNIT_VERSION": "1.15.1",
                            "ASWF_CUDA_VERSION": "10.2",
                            "ASWF_CONAN_CHANNEL": "vfx2020",
                            "ASWF_CONAN_PYTHON_VERSION": "3.9.11",
                            "ASWF_CONAN_VERSION": "1.47.0",
                            "ASWF_DTS_VERSION": "6",
                            "ASWF_GLEW_VERSION": "2.1.0",
                            "ASWF_GLFW_VERSION": "3.1.2",
                            "ASWF_GTEST_VERSION": "1.10.0",
                            "ASWF_HDF5_VERSION": "1.8.21",
                            "ASWF_IMATH_VERSION": "2.4.0",
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
                            "ASWF_PYBIND11_VERSION": "2.4.3",
                            "ASWF_PYSIDE_VERSION": "5.12.6",
                            "ASWF_PYTHON_VERSION": "3.7.3",
                            "ASWF_PYTHON_MAJOR_MINOR_VERSION": "3.7",
                            "ASWF_QT_VERSION": "5.12.6",
                            "ASWF_SONAR_VERSION": "4.6.2.2472",
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
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:{base_versions[1]}",
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
                            "ASWF_VERSION": base_versions[0],
                            "ASWF_BLOSC_VERSION": "1.5.0",
                            "ASWF_BOOST_VERSION": "1.66.0",
                            "ASWF_CCACHE_VERSION": "4.0",
                            "CI_COMMON_VERSION": "1",
                            "ASWF_CLANG_MAJOR_VERSION": "7",
                            "ASWF_CLANG_VERSION": "7.1.0",
                            "ASWF_CMAKE_VERSION": "3.12.4",
                            "ASWF_CPPUNIT_VERSION": "1.14.0",
                            "ASWF_CUDA_VERSION": "10.2",
                            "ASWF_CONAN_CHANNEL": "vfx2019",
                            "ASWF_CONAN_PYTHON_VERSION": "3.9.11",
                            "ASWF_CONAN_VERSION": "1.47.0",
                            "ASWF_DTS_VERSION": "6",
                            "ASWF_GLEW_VERSION": "2.1.0",
                            "ASWF_GLFW_VERSION": "3.1.2",
                            "ASWF_GTEST_VERSION": "1.8.1",
                            "ASWF_HDF5_VERSION": "1.8.21",
                            "ASWF_IMATH_VERSION": "2.3.0",
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
                            "ASWF_PYBIND11_VERSION": "2.4.3",
                            "ASWF_PYSIDE_VERSION": "5.12.6",
                            "ASWF_PYTHON_VERSION": "2.7.15",
                            "ASWF_PYTHON_MAJOR_MINOR_VERSION": "2.7",
                            "ASWF_QT_VERSION": "5.12.6",
                            "ASWF_SONAR_VERSION": "4.6.2.2472",
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
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:{base_versions[0]}",
                            f"{constants.DOCKER_REGISTRY}/aswflocaltesting/ci-base:latest",
                        ],
                        "output": ["type=docker"],
                    },
                },
            },
        )


class TestBuilderCli(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self._log_handlers = logging.getLogger("").handlers
        logging.getLogger("").handlers = []
        self._i = 0

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
        bake_path = os.path.join(
            tempfile.gettempdir(), "docker-bake-PACKAGE-vfx1-2019.json"
        )
        cmd = f"docker buildx bake -f {bake_path} --progress auto"
        self.assertEqual(
            result.output,
            f"INFO:aswfdocker.builder:Would run: '{cmd}'\n",
        )
        self.assertEqual(result.exit_code, 0)

    def test_builder_cli_conan(self):
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
                "--use-conan",
            ],
        )
        self.assertFalse(result.exception)
        bake_path = os.path.join(
            tempfile.gettempdir(), "docker-bake-PACKAGE-vfx1-2019.json"
        )
        cmds = result.output.strip().splitlines()
        self.assertEqual(len(cmds), 4)
        self.assertEqual(
            cmds[0],
            f"INFO:aswfdocker.builder:Would run: 'docker buildx bake -f {bake_path} --progress auto'",
        )
        self.assertTrue(
            cmds[1].startswith(
                "INFO:aswfdocker.builder:Would run: 'docker run -e CONAN_USER_HOME="
                + constants.CONAN_USER_HOME
            ),
            msg=cmds[1],
        )
        self.assertTrue(
            cmds[1].endswith("conan config set general.default_profile=vfx2019'"),
            msg=cmds[1],
        )
        self.assertTrue(
            cmds[2].endswith(
                f"conan create {constants.CONAN_USER_HOME}/recipes/openexr openexr/2.3.0@aswftesting/vfx2019'"
            ),
            msg=cmds[2],
        )
        self.assertEqual(result.exit_code, 0)

    def test_builder_cli_fromtag(self):
        runner = CliRunner()
        result = runner.invoke(
            aswfdocker.cli,
            ["build", "--full-name", "aswftesting/ci-common:1-clang7", "--dry-run"],
        )
        self.assertFalse(result.exception)
        bake_path = os.path.join(
            tempfile.gettempdir(), "docker-bake-IMAGE-common-1-clang7.json"
        )
        cmd = f"docker buildx bake -f {bake_path} --progress auto"
        self.assertEqual(
            result.output,
            f"INFO:aswfdocker.builder:Would run: '{cmd}'\n",
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
        bake_path = os.path.join(
            tempfile.gettempdir(), "docker-bake-PACKAGE-vfx1-2019-2020.json"
        )
        cmd = f"docker buildx bake -f {bake_path} --progress auto"
        self.assertEqual(
            result.output,
            f"INFO:aswfdocker.builder:Would run: '{cmd}'\n",
        )
        self.assertEqual(result.exit_code, 0)

    def _assertEndsWith(self, cmds, expected):
        self.assertTrue(cmds[self._i].endswith(expected), "got: " + cmds[self._i])
        self._i += 1

    def test_builderlist_cli_conan(self):
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
                "--use-conan",
                "--keep-source",
                "--keep-build",
                "--conan-login",
                "--build-missing",
                "--push",
                "YES",
            ],
        )
        self.assertFalse(result.exception, msg=result.output)
        bake_path = os.path.join(
            tempfile.gettempdir(), "docker-bake-PACKAGE-vfx1-2019-2020.json"
        )
        cmds = result.output.strip().splitlines()
        self.assertEqual(len(cmds), 13)
        self.assertEqual(
            cmds[self._i],
            f"INFO:aswfdocker.builder:Would run: 'docker buildx bake -f {bake_path} --progress auto'",
        )
        self._i += 1
        self.assertTrue(
            cmds[self._i].startswith(
                "INFO:aswfdocker.builder:Would run: 'docker run -e CONAN_USER_HOME="
                + constants.CONAN_USER_HOME
            ),
            msg=cmds[self._i],
        )
        self._assertEndsWith(cmds, "conan user -p -r aswftesting'")
        self._assertEndsWith(cmds, "conan config set general.default_profile=vfx2019'")
        self._assertEndsWith(
            cmds,
            f"conan create {constants.CONAN_USER_HOME}/recipes/openexr"
            " openexr/2.3.0@aswftesting/vfx2019"
            " --keep-source --keep-build --build=missing'",
        )
        self._assertEndsWith(
            cmds,
            "conan alias openexr/latest@aswftesting/vfx2019"
            " openexr/2.3.0@aswftesting/vfx2019'",
        )
        self._assertEndsWith(
            cmds,
            "conan upload --all -r aswftesting" " openexr/2.3.0@aswftesting/vfx2019'",
        )
        self._assertEndsWith(
            cmds,
            "conan upload --all -r aswftesting" " openexr/latest@aswftesting/vfx2019'",
        )
        self._assertEndsWith(cmds, "conan user -p -r aswftesting'")
        self._assertEndsWith(cmds, "conan config set general.default_profile=vfx2020'")
        self._assertEndsWith(
            cmds,
            f"conan create {constants.CONAN_USER_HOME}/recipes/openexr"
            " openexr/2.4.0@aswftesting/vfx2020"
            " --keep-source --keep-build --build=missing'",
        )
        self.assertEqual(result.exit_code, 0)

    def test_builder_cli_allversions(self):
        runner = CliRunner()
        result = runner.invoke(
            aswfdocker.cli,
            ["build", "--group", "common", "--version", "all", "--dry-run"],
        )
        self.assertFalse(result.exception)
        bake_path = os.path.join(
            tempfile.gettempdir(),
            "docker-bake-IMAGE-common-1-clang10-1-clang6-1-clang7-1"
            "-clang8-1-clang9-2-clang10-2-clang11-2-clang12-2-clang13-2-clang14.json",
        )
        cmd = f"docker buildx bake -f {bake_path} --progress auto"
        self.assertEqual(
            result.output,
            f"INFO:aswfdocker.builder:Would run: '{cmd}'\n",
        )
        self.assertEqual(result.exit_code, 0)
