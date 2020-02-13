import logging
import subprocess
import json
import os
import tempfile

from . import constants, buildinfo

logger = logging.getLogger("build-packages")


class Builder:
    def __init__(
        self,
        build_info: buildinfo.BuildInfo,
        image_type: constants.IMAGE_TYPE,
        dry_run: bool = False,
        group_name: str = "",
        group_version: str = "",
        push: bool = False,
        target: str = "",
        progress: bool = "",
    ):
        self.dry_run = dry_run
        self.group_name = group_name
        self.group_version = group_version
        self.push = push
        self.build_info = build_info
        self.image_type = image_type
        self.target = target
        self.progress = progress

    def make_bake_dict(self) -> dict:
        targets = {}
        for img in constants.GROUPS[self.image_type][self.group_name]:
            if self.target and img != self.target:
                logger.debug("Skipping target %s", img)
                continue
            if self.image_type == constants.IMAGE_TYPE.PACKAGE:
                dockerName = f"ci-package-{img}"
                dockerFile = "packages/Dockerfile"
                target = f"ci-{img}-package"
                targetName = f"package-{img}"
            else:
                dockerName = f"ci-{img}"
                dockerFile = f"{dockerName}/Dockerfile"
                target = ""
                targetName = f"image-{img}"

            fullVersions = constants.VERSIONS[self.image_type][img]
            majorVersions = [v.split(".")[0] for v in fullVersions]
            if self.group_version in majorVersions:
                versionInfo = constants.VERSION_INFO[self.group_version]
                aswf_version = fullVersions[majorVersions.index(self.group_version)]
                tags = [
                    versionInfo.version,
                    aswf_version,
                ]
                if versionInfo.label:
                    tags.append(versionInfo.label)
                tags = list(
                    map(
                        lambda tag: f"docker.io/{self.build_info.dockerOrg}/{dockerName}:{tag}",
                        tags,
                    )
                )

                targetDict = {
                    "context": ".",
                    "dockerfile": dockerFile,
                    "args": {
                        "ASWF_ORG": self.build_info.dockerOrg,
                        "ASWF_PKG_ORG": self.build_info.pkgOrg,
                        "ASWF_VERSION": aswf_version,
                        "CI_COMMON_VERSION": versionInfo.ciCommonVersion,
                        "PYTHON_VERSION": versionInfo.pythonVersion,
                        "BUILD_DATE": "dev",
                        "VCS_REF": "dev",
                        "VFXPLATFORM_VERSION": self.group_version,
                    },
                    "tags": tags,
                    "output": [
                        "type=registry,push=true" if self.push else "type=docker"
                    ],
                }
                if target:
                    targetDict["target"] = target
                targets[targetName] = targetDict

        root = {}
        root["target"] = targets
        root["group"] = {"default": {"targets": list(targets.keys())}}
        return root

    def make_bake_jsonfile(self) -> str:
        d = self.make_bake_dict()
        path = os.path.join(
            tempfile.gettempdir(),
            f"docker-bake-{self.image_type.name}-{self.group_name}-{self.group_version}.json",
        )
        with open(path, "w") as f:
            json.dump(d, f, indent=4, sort_keys=True)
        return path

    def build(self) -> None:
        path = self.make_bake_jsonfile()
        cmd = f"docker buildx bake -f {path} --progress {self.progress}"
        logger.debug("Repo root: %s", self.build_info.repo_root)
        if self.dry_run:
            logger.info("Would build: %r", cmd)
        else:
            logger.info("Building: %r", cmd)
            subprocess.run(
                cmd, shell=True, check=True, cwd=self.build_info.repo_root
            )
