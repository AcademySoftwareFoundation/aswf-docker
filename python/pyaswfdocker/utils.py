import subprocess
import datetime


def get_current_branch() -> str:
    return subprocess.check_output("git rev-parse --abbrev-ref HEAD", encoding="UTF-8")


def get_current_sha() -> str:
    return subprocess.check_output("git rev-parse --short HEAD", encoding="UTF-8")


def get_current_date() -> str:
    # 2020-01-19T08:04:51Z
    return datetime.datetime.now().isoformat(timespec="seconds") + "Z"
