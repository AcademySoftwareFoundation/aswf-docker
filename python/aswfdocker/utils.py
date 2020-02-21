# SPDX-License-Identifier: Apache-2.0
"""
Utility functions
"""
import os
import subprocess
import datetime

from aswfdocker import constants


def get_current_branch() -> str:
    return subprocess.check_output("git rev-parse --abbrev-ref HEAD", encoding="UTF-8")


def get_current_sha() -> str:
    return subprocess.check_output("git rev-parse --short HEAD", encoding="UTF-8")


def get_current_date() -> str:
    # 2020-01-19T08:04:51Z
    return datetime.datetime.now().isoformat(timespec="seconds") + "Z"


def get_docker_org(repo_uri: str, source_branch: str) -> str:
    if not source_branch and not repo_uri:
        return constants.TESTING_DOCKER_ORG
    if (
        source_branch == "refs/heads/master"
        and repo_uri == constants.MAIN_GITHUB_ASWF_DOCKER_URL
    ):
        docker_org = constants.PUBLISH_DOCKER_ORG
    elif source_branch in ("refs/heads/testing", ""):
        docker_org = constants.TESTING_DOCKER_ORG
    else:
        docker_org = constants.FAKE_DOCKER_ORG
    return docker_org


def get_docker_push(repo_uri: str, source_branch: str) -> str:
    if (
        source_branch == "refs/heads/master"
        and repo_uri == constants.MAIN_GITHUB_ASWF_DOCKER_URL
    ) or source_branch == "refs/heads/testing":
        return "true"
    return "false"


def get_major_version(version: str) -> str:
    return version.split(".")[0]


def download_package(repo_root: str, docker_org: str, package: str, version: str):
    folder = os.path.join(repo_root, "packages", version)
    os.makedirs(folder)
    subprocess.check_call(
        f"docker pull {docker_org}/ci-package-{package}:{version}", shell=True
    )
    container_id = subprocess.check_output(
        f"docker create {docker_org}/ci-package-{package}:{version} null", shell=True
    ).decode("utf-8")
    output = os.path.join(folder, package + ".tar")
    subprocess.check_call(f"docker export --output={output} {container_id}", shell=True)
    subprocess.check_call(f"docker rm {container_id}", shell=True)
    subprocess.check_call(f"gzip -9 {output}", shell=True)
    return output + ".gz"


def get_image_name(image_type: constants.ImageType, image: str):
    if image_type == constants.ImageType.PACKAGE:
        return f"ci-package-{image}"
    return f"ci-{image}"
