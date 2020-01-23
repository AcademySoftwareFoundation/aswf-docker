import typing


class VersionInfo:
    def __init__(
        self,
        version: str,
        aswfVersion: str,
        label: typing.Optional[str],
        ciCommonVersion: str,
        pythonVersion: str,
    ):
        self.version = version
        self.aswfVersion = aswfVersion
        self.ciCommonVersion = ciCommonVersion
        self.label = label
        self.pythonVersion = pythonVersion
