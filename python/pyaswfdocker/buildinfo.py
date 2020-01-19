class BuildInfo:
    def __init__(
        self,
        dockerOrg: str = "",
        pkgOrg: str = "",
        aswfVersion: str = "",
        ciCommonVersion: str = "",
    ):
        self.dockerOrg = dockerOrg
        if pkgOrg is None:
            pkgOrg = dockerOrg
        self.pkgOrg = pkgOrg
        self.aswfVersion = aswfVersion
        self.ciCommonVersion = ciCommonVersion
