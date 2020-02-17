import logging
import subprocess
import json
import os
import tempfile

from aswfdocker import constants, buildinfo, utils

logger = logging.getLogger(__name__)


class GroupInfo:
    def __init__(
        self,
        type_: constants.ImageType,
        name: str = "",
        version: str = "",
        target: str = "",
    ):
        self.type = type_
        self.name = name
        self.version = version
        if name not in constants.GROUPS[self.type]:
            raise TypeError(f"Group {name} is not valid!")
        self.images = constants.GROUPS[self.type][name]
        self.target = target


class Builder:
    def __init__(
        self,
        build_info: buildinfo.BuildInfo,
        group_info: GroupInfo,
        push: bool = False,
    ):
        self.push = push
        self.build_info = build_info
        self.group_info = group_info

    def make_bake_dict(self) -> dict:
        targets = {}
        for img in self.group_info.images:
            if self.group_info.target and img != self.group_info.target:
                logger.debug("Skipping target %s", img)
                continue

            image_name = utils.get_image_name(self.group_info.type, img)
            if self.group_info.type == constants.ImageType.PACKAGE:
                docker_file = "packages/Dockerfile"
                target = f"ci-{img}-package"
                target_name = f"package-{img}"
            else:
                docker_file = f"{image_name}/Dockerfile"
                target = ""
                target_name = f"image-{img}"

            versions = constants.VERSIONS[self.group_info.type][img]
            major_versions = [utils.get_major_version(v) for v in versions]
            if self.group_info.version in major_versions:
                version_info = constants.VERSION_INFO[self.group_info.version]
                aswf_version = versions[major_versions.index(self.group_info.version)]
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
                        "VFXPLATFORM_VERSION": self.group_info.version,
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
            f"docker-bake-{self.group_info.type.name}-{self.group_info.name}-{self.group_info.version}.json",
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
