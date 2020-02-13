import subprocess
import datetime
from . import constants


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
        and repo_uri == "https://github.com/AcademySoftwareFoundation/aswf-docker"
    ):
        dockerOrg = constants.PUBLISH_DOCKER_ORG
    elif source_branch in ("refs/heads/testing", ""):
        dockerOrg = constants.TESTING_DOCKER_ORG
    else:
        dockerOrg = constants.FAKE_DOCKER_ORG
    return dockerOrg


def get_repo_root_path(repo_rootPath):
    return repo_rootPath
