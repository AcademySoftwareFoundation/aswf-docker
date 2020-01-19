import logging
import subprocess
import json
import os

from pyaswfdocker import constants, buildinfo

logger = logging.getLogger("build-packages")


class Builder:
    def __init__(
        self,
        buildInfo: buildinfo.BuildInfo,
        dryRun: bool = False,
        groupName: str = "",
        groupVersion: str = "",
        push: bool = False,
    ):
        self.dryRun = dryRun
        self.groupName = groupName
        self.groupVersion = groupVersion
        self.push = push
        self.buildInfo = buildInfo

    def make_bake_dict(self) -> dict:
        targets = {}
        for pkg in constants.PACKAGE_GROUPS[self.groupName]:
            if self.groupVersion in constants.PACKAGES[pkg]:
                target = {
                    "context": ".",
                    "dockerfile": "packages/Dockerfile",
                    "args": {
                        "ASWF_ORG": self.buildInfo.dockerOrg,
                        "ASWF_PKG_ORG": self.buildInfo.pkgOrg,
                        "ASWF_VERSION": self.buildInfo.aswfVersion,
                        "CI_COMMON_VERSION": self.buildInfo.ciCommonVersion,
                        "PYTHON_VERSION": constants.PYTHON_VERSIONS[self.groupVersion],
                        "BUILD_DATE": "dev",
                        "VCS_REF": "dev",
                        "VFXPLATFORM_VERSION": self.groupVersion,
                    },
                    "tags": [
                        f"docker.io/{self.buildInfo.dockerOrg}/ci-package-{pkg}:{self.groupVersion}",
                        f"docker.io/{self.buildInfo.dockerOrg}/ci-package-{pkg}:{self.buildInfo.aswfVersion}",
                    ],
                    "target": f"ci-base-{pkg}-package",
                    "output": ["type=docker"],
                }
                targets[f"package-{pkg}"] = target
        root = {}
        root["target"] = targets
        root["group"] = {"default": {"targets": list(targets.keys())}}
        return root

    def make_bake_jsonfile(self) -> str:
        d = self.make_bake_dict()
        path = os.path.join(
            "packages", f"docker-bake-{self.groupName}-{self.groupVersion}.json"
        )
        with open(path, "w") as f:
            json.dump(d, f, indent=4, sort_keys=True)
        return path

    def build(self) -> None:
        path = self.make_bake_jsonfile()
        cmd = f"docker buildx bake -f {path}"
        logger.info("Building %r", cmd)
        subprocess.run(
            cmd, shell=True, check=True,
        )
