import unittest
from pyaswfdocker import builder, buildinfo


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.buildInfo = buildinfo.BuildInfo(repoUri="notauri", sourceBranch="testing",)

    def test_package_baseqt_2019_dict(self):
        b = builder.Builder(
            self.buildInfo,
            groupName="baseqt",
            groupVersion="2019",
            imageType="packages",
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
                            "ASWF_VERSION": "2019.1",
                            "BUILD_DATE": "dev",
                            "CI_COMMON_VERSION": "1",
                            "PYTHON_VERSION": "2.7",
                            "VCS_REF": "dev",
                            "VFXPLATFORM_VERSION": "2019",
                        },
                        "tags": [
                            "docker.io/aswflocaltesting/ci-package-qt:2019",
                            "docker.io/aswflocaltesting/ci-package-qt:2019.1",
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
            self.buildInfo, groupName="base", groupVersion="2019", imageType="images",
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
                            "ASWF_VERSION": "2019.1",
                            "BUILD_DATE": "dev",
                            "CI_COMMON_VERSION": "1",
                            "PYTHON_VERSION": "2.7",
                            "VCS_REF": "dev",
                            "VFXPLATFORM_VERSION": "2019",
                        },
                        "tags": [
                            "docker.io/aswflocaltesting/ci-base:2019",
                            "docker.io/aswflocaltesting/ci-base:2019.1",
                            "docker.io/aswflocaltesting/ci-base:latest",
                        ],
                        "output": ["type=docker"],
                    }
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
