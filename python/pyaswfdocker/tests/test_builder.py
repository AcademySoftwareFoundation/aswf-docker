import unittest
from pyaswfdocker import builder, buildinfo


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.buildInfo = buildinfo.BuildInfo(
            repoUri="notauri",
            sourceBranch="testing",
            aswfVersion="2019.0",
            ciCommonVersion="1",
        )
        self.baseqt2019Dict = {
            "group": {"default": {"targets": ["package-qt"]}},
            "target": {
                "package-qt": {
                    "context": ".",
                    "dockerfile": "packages/Dockerfile",
                    "args": {
                        "ASWF_ORG": "aswflocaltesting",
                        "ASWF_PKG_ORG": "aswftesting",
                        "ASWF_VERSION": "2019.0",
                        "BUILD_DATE": "dev",
                        "CI_COMMON_VERSION": "1",
                        "PYTHON_VERSION": "2.7",
                        "VCS_REF": "dev",
                        "VFXPLATFORM_VERSION": "2019",
                    },
                    "tags": [
                        "docker.io/aswflocaltesting/ci-package-qt:2019",
                        "docker.io/aswflocaltesting/ci-package-qt:2019.0",
                    ],
                    "target": "ci-base-qt-package",
                    "output": ["type=docker"],
                }
            },
        }

    def test_baseqt_2019_dict(self):
        b = builder.Builder(self.buildInfo, groupName="baseqt", groupVersion="2019",)
        self.assertEqual(
            b.make_bake_dict(), self.baseqt2019Dict,
        )


if __name__ == "__main__":
    unittest.main()
