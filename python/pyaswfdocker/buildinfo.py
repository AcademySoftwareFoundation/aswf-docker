from . import utils, constants


class BuildInfo:
    def __init__(
        self,
        repo_uri: str = "",
        source_branch: str = "",
        aswf_version: str = "",
        repo_root: str = "",
    ):
        self.aswf_version = aswf_version
        self.repo_uri = repo_uri
        self.source_branch = source_branch
        self.dockerOrg = utils.get_docker_org(repo_uri, source_branch)
        self.repo_root = utils.get_repo_root_path(repo_root)
        if self.dockerOrg == constants.FAKE_DOCKER_ORG:
            self.pkgOrg = constants.TESTING_DOCKER_ORG
        else:
            self.pkgOrg = self.dockerOrg
        if self.dockerOrg == constants.PUBLISH_DOCKER_ORG:
            self.vcfRef = utils.get_current_sha()
            self.buildDate = utils.get_current_date()
        else:
            self.vcfRef = "dev"
            self.buildDate = "dev"
