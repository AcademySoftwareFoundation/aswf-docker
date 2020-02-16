from aswfdocker import utils, constants


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
        self.docker_org = utils.get_docker_org(repo_uri, source_branch)
        self.repo_root = utils.get_repo_root_path(repo_root)
        if self.docker_org == constants.FAKE_DOCKER_ORG:
            self.package_org = constants.TESTING_DOCKER_ORG
        else:
            self.package_org = self.docker_org
        if self.docker_org == constants.PUBLISH_DOCKER_ORG:
            self.vcs_ref = utils.get_current_sha()
            self.build_date = utils.get_current_date()
        else:
            self.vcs_ref = "dev"
            self.build_date = "dev"
