import unittest
import logging
import tempfile

from click.testing import CliRunner

from aswfdocker import builder, buildinfo, constants
from aswfdocker.cli import aswfdocker


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.build_info = buildinfo.BuildInfo(
            repo_uri="notauri", source_branch="testing", aswf_version="2019.123"
        )

    def test_package_baseqt_2019_dict(self):
        b = builder.Builder(
            self.build_info,
            builder.GroupInfo(
                name="baseqt", version="2019", type_=constants.ImageType.PACKAGE,
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
                            "BUILD_DATE": "dev",
                            "CI_COMMON_VERSION": "1",
                            "PYTHON_VERSION": "2.7",
                            "VCS_REF": "dev",
                            "VFXPLATFORM_VERSION": "2019",
                        },
                        "tags": [
                            "docker.io/aswflocaltesting/ci-package-qt:2019",
                            f"docker.io/aswflocaltesting/ci-package-qt:{constants.VERSIONS[constants.ImageType.PACKAGE]['qt'][1]}",
                            "docker.io/aswflocaltesting/ci-package-qt:latest",
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
                name="base", version="2019", type_=constants.ImageType.IMAGE,
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
                            "BUILD_DATE": "dev",
                            "CI_COMMON_VERSION": "1",
                            "PYTHON_VERSION": "2.7",
                            "VCS_REF": "dev",
                            "VFXPLATFORM_VERSION": "2019",
                        },
                        "tags": [
                            "docker.io/aswflocaltesting/ci-base:2019",
                            f"docker.io/aswflocaltesting/ci-base:{constants.VERSIONS[constants.ImageType.IMAGE]['base'][1]}",
                            "docker.io/aswflocaltesting/ci-base:latest",
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
