import typing


class VersionInfo:
    def __init__(
        self,
        major_version: str,
        label: typing.Optional[str],
        ci_common_version: str,
        python_version: str,
    ):
        self.major_version = major_version
        self.ci_common_version = ci_common_version
        self.label = label
        self.python_version = python_version

    def get_tags(
        self, aswf_version: str, docker_org: str, image_name: str
    ) -> typing.List[str]:
        tags = [
            self.major_version,
            aswf_version,
        ]
        if self.label:
            tags.append(self.label)
        return list(
            map(lambda tag: f"docker.io/{docker_org}/{image_name}:{tag}", tags)
        )
