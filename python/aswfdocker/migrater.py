import logging
import subprocess

from aswfdocker import constants, utils

logger = logging.getLogger(__name__)


class Migrater:
    def __init__(self, from_org: str, to_org: str):
        self.from_org = from_org
        self.to_org = to_org
        self.migration_list = []
        self.cmds = []

    def gather(self, package: str, version: str):
        for pkg, versions in constants.VERSIONS[constants.IMAGE_TYPE.PACKAGE].items():
            image = "ci-package-" + pkg
            if not package or package == pkg:
                for v in versions:
                    majorVersion = v.split(".")[0]
                    if not version or version == majorVersion:
                        from_pkg = f"docker.io/{self.from_org}/{image}:{v}"
                        to_pkg = f"docker.io/{self.to_org}/{image}:{v}"
                        self.migration_list.append((image, v, from_pkg, to_pkg))

    def migrate(self, dry_run: bool):
        for image, version, from_pkg, to_pkg in self.migration_list:
            if dry_run:
                logger.info("Migrating %s -> %s", from_pkg, to_pkg)
            else:
                logger.info("Would migrate %s -> %s", from_pkg, to_pkg)

            self.cmds.append(f"docker pull {from_pkg}")
            self.cmds.append(f"docker tag {from_pkg} {to_pkg}")

            majorVersion = utils.get_major_version(version)
            versionInfo = constants.VERSION_INFO[majorVersion]
            tags = versionInfo.get_tags(version, self.to_org, image)
            if len(tags) > 1:
                for tag in tags:
                    if tag != to_pkg:
                        self.cmds.append(f"docker tag {to_pkg} {tag}")

            self.cmds.append(f"docker push {to_pkg}")

        if logger.isEnabledFor(logging.DEBUG):
            list(map(logger.debug, self.cmds))

        if not dry_run:
            for cmd in self.cmds:
                subprocess.run(cmd, shell=True, check=True)
