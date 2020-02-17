import unittest
import logging

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

    def test_cli_getdockerorg(self):
        runner = CliRunner()
        result = runner.invoke(aswfdocker.cli, ["getdockerorg"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "aswftesting\n")

    def test_cli_getdockerpush(self):
        runner = CliRunner()
        result = runner.invoke(aswfdocker.cli, ["getdockerpush"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "false\n")
