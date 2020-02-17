import unittest
import logging
import tempfile
import os

from click.testing import CliRunner

from aswfdocker import utils
from aswfdocker.cli import aswfdocker


class TestUtils(unittest.TestCase):
    def test_get_docker_org(self):
        self.assertEqual(utils.get_docker_org("", ""), "aswftesting")
        self.assertEqual(
            utils.get_docker_org(
                "https://github.com/AcademySoftwareFoundation/aswf-docker",
                "refs/heads/master",
            ),
            "aswf",
        )
        self.assertEqual(
            utils.get_docker_org(
                "https://github.com/AcademySoftwareFoundation/aswf-docker",
                "refs/heads/testing",
            ),
            "aswftesting",
        )
        self.assertEqual(
            utils.get_docker_org(
                "https://github.com/randomfork/aswf-docker", "refs/heads/master"
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
        self.assertEqual(utils.get_docker_push("", ""), "false")
        self.assertEqual(
            utils.get_docker_push(
                "https://github.com/AcademySoftwareFoundation/aswf-docker",
                "refs/heads/master",
            ),
            "true",
        )
        self.assertEqual(
            utils.get_docker_push(
                "https://github.com/AcademySoftwareFoundation/aswf-docker",
                "refs/heads/testing",
            ),
            "true",
        )
        self.assertEqual(
            utils.get_docker_push(
                "https://github.com/randomfork/aswf-docker", "refs/heads/master"
            ),
            "false",
        )
        self.assertEqual(
            utils.get_docker_push(
                "https://github.com/randomfork/aswf-docker", "refs/heads/randombranch"
            ),
            "false",
        )


class TestUtilsCli(unittest.TestCase):
    def setUp(self):
        logging.getLogger("").handlers = []
        self.maxDiff = None

    def test_cli_getdockerorg(self):
        runner = CliRunner()
        result = runner.invoke(aswfdocker.cli, ["getdockerorg"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "aswftesting")

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
            self.assertEqual(result.output, f"{tmpdirname}/packages/2019/tbb.tar.gz")
            self.assertTrue(os.path.exists(result.output))

    def test_cli_packages(self):
        runner = CliRunner()
        result = runner.invoke(aswfdocker.cli, ["packages"], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        pkgs = result.output.split("\n")
        self.assertGreater(len(pkgs), 20)
        self.assertEqual(pkgs[0], "common/ci-package-clang:1.1")

    def test_cli_images(self):
        runner = CliRunner()
        result = runner.invoke(aswfdocker.cli, ["images"], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        imgs = result.output.split("\n")
        self.assertGreater(len(imgs), 15)
        self.assertEqual(imgs[0], "common/ci-common:1.1")
