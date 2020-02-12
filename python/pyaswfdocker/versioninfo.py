import typing


class VersionInfo:
    def __init__(
        self,
        version: str,
        label: typing.Optional[str],
        ciCommonVersion: str,
        pythonVersion: str,
    ):
        self.version = version
        self.ciCommonVersion = ciCommonVersion
        self.label = label
        self.pythonVersion = pythonVersion
