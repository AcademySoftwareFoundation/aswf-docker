import logging
import subprocess
import json
import os
import tempfile

from aswfdocker import constants, buildinfo, utils

logger = logging.getLogger(__name__)


class Builder:
    def __init__(
        self,
        build_info: buildinfo.BuildInfo,
        image_type: constants.IMAGE_TYPE,
        group_name: str = "",
        group_version: str = "",
        target: str = "",
        push: bool = False,
    ):
        self.group_name = group_name
        self.group_version = group_version
        self.push = push
        self.build_info = build_info
        self.image_type = image_type
        self.target = target

    def make_bake_dict(self) -> dict:
        targets = {}
        for img in constants.GROUPS[self.image_type][self.group_name]:
            if self.target and img != self.target:
                logger.debug("Skipping target %s", img)
                continue
            if self.image_type == constants.IMAGE_TYPE.PACKAGE:
                image_name = f"ci-package-{img}"
                docker_file = "packages/Dockerfile"
                target = f"ci-{img}-package"
                target_name = f"package-{img}"
            else:
                image_name = f"ci-{img}"
                docker_file = f"{image_name}/Dockerfile"
                target = ""
                target_name = f"image-{img}"

            versions = constants.VERSIONS[self.image_type][img]
            major_versions = [utils.get_major_version(v) for v in versions]
            if self.group_version in major_versions:
                version_info = constants.VERSION_INFO[self.group_version]
                aswf_version = versions[major_versions.index(self.group_version)]
                tags = version_info.get_tags(
                    aswf_version, self.build_info.docker_org, image_name
                )
                target_dict = {
                    "context": ".",
                    "dockerfile": docker_file,
                    "args": {
                        "ASWF_ORG": self.build_info.docker_org,
                        "ASWF_PKG_ORG": self.build_info.package_org,
                        "ASWF_VERSION": aswf_version,
                        "CI_COMMON_VERSION": version_info.ci_common_version,
                        "PYTHON_VERSION": version_info.python_version,
                        "BUILD_DATE": self.build_info.build_date,
                        "VCS_REF": self.build_info.vcs_ref,
                        "VFXPLATFORM_VERSION": self.group_version,
                    },
                    "tags": tags,
                    "output": [
                        "type=registry,push=true" if self.push else "type=docker"
                    ],
                }
                if target:
                    target_dict["target"] = target
                targets[target_name] = target_dict

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

    def build(self, dry_run: bool = False, progress: str = "") -> None:
        path = self.make_bake_jsonfile()
        cmd = f"docker buildx bake -f {path} --progress {progress}"
        logger.debug("Repo root: %s", self.build_info.repo_root)
        if dry_run:
            logger.info("Would build: %r", cmd)
        else:
            logger.info("Building: %r", cmd)
            subprocess.run(cmd, shell=True, check=True, cwd=self.build_info.repo_root)
