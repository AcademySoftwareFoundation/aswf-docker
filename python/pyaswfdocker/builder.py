import logging
import argparse
import subprocess
import json
import os

from . import constants

logger = logging.getLogger("build-packages")


class Builder:
    def __init__(
        self,
        dryRun=False,
        groupName=None,
        groupVersion=None,
        push=False,
        dockerOrg=None,
        pkgOrg=None,
        aswfVersion=None,
        ciCommonVersion=None,
    ):
        self.dryRun = dryRun
        self.groupName = groupName
        self.groupVersion = groupVersion
        self.push = push
        self.dockerOrg = dockerOrg
        if pkgOrg is None:
            pkgOrg = dockerOrg
        self.pkgOrg = pkgOrg
        self.aswfVersion = aswfVersion
        self.ciCommonVersion = ciCommonVersion

    def make_bake_dict(self):
        targets = {}
        for pkg in constants.PACKAGE_GROUPS[self.groupName]:
            if self.groupVersion in constants.PACKAGES[pkg]:
                target = {
                    "context": ".",
                    "dockerfile": "packages/Dockerfile",
                    "args": {
                        "ASWF_ORG": self.dockerOrg,
                        "ASWF_PKG_ORG": self.pkgOrg,
                        "ASWF_VERSION": self.aswfVersion,
                        "CI_COMMON_VERSION": self.ciCommonVersion,
                        "PYTHON_VERSION": constants.PYTHON_VERSIONS[self.groupVersion],
                        "BUILD_DATE": "dev",
                        "VCS_REF": "dev",
                        "VFXPLATFORM_VERSION": self.groupVersion,
                    },
                    "tags": [
                        f"docker.io/{self.dockerOrg}/ci-package-{pkg}:{self.groupVersion}",
                        f"docker.io/{self.dockerOrg}/ci-package-{pkg}:{self.aswfVersion}",
                    ],
                    "target": f"ci-base-{pkg}-package",
                    "output": ["type=docker"],
                }
                targets[f"package-{pkg}"] = target
        root = {}
        root["target"] = targets
        root["group"] = {"default": {"targets": list(targets.keys())}}
        return root

    def make_bake_json(self):
        d = self.make_bake_dict()
        path = os.path.join(
            "packages", f"docker-bake-{self.groupName}-{self.groupVersion}.json"
        )
        with open(path, "w") as f:
            json.dump(d, f, indent=4, sort_keys=True)
        return path

    def build(self):
        path = self.make_bake_json()
        cmd = f"docker buildx bake -f {path}"
        logger.info("Building %r", cmd)
        subprocess.run(
            cmd, shell=True, check=True,
        )
