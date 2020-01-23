from . import utils, constants


class BuildInfo:
    def __init__(
        self, repoUri: str = "", sourceBranch: str = "",
    ):
        self.repoUri = repoUri
        self.sourceBranch = sourceBranch
        self.dockerOrg = utils.get_docker_org(repoUri, sourceBranch)
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
