import unittest
import json
from pyaswfdocker import builder


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.baseqt2019Dict = {
            "group": {"default": {"targets": ["package-qt"]}},
            "target": {
                "package-qt": {
                    "context": ".",
                    "dockerfile": "packages/Dockerfile",
                    "args": {
                        "ASWF_ORG": "aswftesting",
                        "ASWF_PKG_ORG": "aswf",
                        "ASWF_VERSION": "2019.0",
                        "BUILD_DATE": "dev",
                        "CI_COMMON_VERSION": "1",
                        "PYTHON_VERSION": "2.7",
                        "VCS_REF": "dev",
                        "VFXPLATFORM_VERSION": "2019",
                    },
                    "tags": [
                        "docker.io/aswftesting/ci-package-qt:2019",
                        "docker.io/aswftesting/ci-package-qt:2019.0",
                    ],
                    "target": "ci-base-qt-package",
                    "output": ["type=docker"],
                }
            },
        }

    def test_baseqt_2019_dict(self):
        b = builder.Builder(
            groupName="baseqt",
            groupVersion="2019",
            dockerOrg="aswftesting",
            pkgOrg="aswf",
            aswfVersion="2019.0",
            ciCommonVersion="1",
        )
        self.assertEqual(
            b.make_bake_dict(), self.baseqt2019Dict,
        )


if __name__ == "__main__":
    unittest.main()
