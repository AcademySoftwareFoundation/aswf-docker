import unittest
from pyaswfdocker import builder, buildinfo, constants


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.build_info = buildinfo.BuildInfo(
            repo_uri="notauri", source_branch="testing", aswf_version="2019.123"
        )

    def test_package_baseqt_2019_dict(self):
        b = builder.Builder(
            self.build_info,
            group_name="baseqt",
            group_version="2019",
            image_type=constants.IMAGE_TYPE.PACKAGE,
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
                            "ASWF_VERSION": constants.VERSIONS[constants.IMAGE_TYPE.PACKAGE]["qt"][1],
                            "BUILD_DATE": "dev",
                            "CI_COMMON_VERSION": "1",
                            "PYTHON_VERSION": "2.7",
                            "VCS_REF": "dev",
                            "VFXPLATFORM_VERSION": "2019",
                        },
                        "tags": [
                            "docker.io/aswflocaltesting/ci-package-qt:2019",
                            f"docker.io/aswflocaltesting/ci-package-qt:{constants.VERSIONS[constants.IMAGE_TYPE.PACKAGE]['qt'][1]}",
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
            group_name="base",
            group_version="2019",
            image_type=constants.IMAGE_TYPE.IMAGE,
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
                            "ASWF_VERSION": constants.VERSIONS[constants.IMAGE_TYPE.IMAGE]["base"][1],
                            "BUILD_DATE": "dev",
                            "CI_COMMON_VERSION": "1",
                            "PYTHON_VERSION": "2.7",
                            "VCS_REF": "dev",
                            "VFXPLATFORM_VERSION": "2019",
                        },
                        "tags": [
                            "docker.io/aswflocaltesting/ci-base:2019",
                            f"docker.io/aswflocaltesting/ci-base:{constants.VERSIONS[constants.IMAGE_TYPE.IMAGE]['base'][1]}",
                            "docker.io/aswflocaltesting/ci-base:latest",
                        ],
                        "output": ["type=docker"],
                    }
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
