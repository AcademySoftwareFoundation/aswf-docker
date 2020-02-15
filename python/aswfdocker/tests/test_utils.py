import unittest
from aswfdocker import utils


class TestBuilder(unittest.TestCase):
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
