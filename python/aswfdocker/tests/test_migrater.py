import unittest
from aswfdocker import migrater, constants


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_migrate_nofilter(self):
        m = migrater.Migrater("src", "dst")
        m.gather("", "")
        self.assertGreater(len(m.migration_list), 10)

    def test_migrate_pkgfilter(self):
        m = migrater.Migrater("src", "dst")
        m.gather("openexr", "")
        self.assertEqual(len(m.migration_list), 3)

    def test_migrate_versionfilter(self):
        m = migrater.Migrater("src", "dst")
        m.gather("openexr", "2019")
        current_version = constants.VERSIONS[constants.IMAGE_TYPE.PACKAGE]["qt"][1]
        self.assertEqual(
            m.migration_list,
            [
                (
                    "ci-package-openexr",
                    "2019.1",
                    f"docker.io/src/ci-package-openexr:{current_version}",
                    f"docker.io/dst/ci-package-openexr:{current_version}",
                )
            ],
        )
        m.migrate(dry_run=True)
        self.assertEqual(
            m.cmds,
            [
                f"docker pull docker.io/src/ci-package-openexr:{current_version}",
                f"docker tag docker.io/src/ci-package-openexr:{current_version} docker.io/dst/ci-package-openexr:{current_version}",
                f"docker tag docker.io/dst/ci-package-openexr:{current_version} docker.io/dst/ci-package-openexr:2019",
                f"docker tag docker.io/dst/ci-package-openexr:{current_version} docker.io/dst/ci-package-openexr:latest",
                f"docker push docker.io/dst/ci-package-openexr:{current_version}",
            ],
        )
