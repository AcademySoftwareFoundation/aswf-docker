#!/usr/bin/env python3

import logging
import argparse
import subprocess

from .. import constants

logger = logging.getLogger("migrate-packages")


def migrate(args):
    fromOrg = args.fromOrg
    toOrg = args.toOrg
    for pkg, versions in constants.VERSIONS["packages"].items():
        for version in versions:
            fromPkg = f"{fromOrg}/ci-package-{pkg}:{version}"
            toPkg = f"{toOrg}/ci-package-{pkg}:{version}"
            logger.info("Migrating %s -> %s", fromPkg, toPkg)
            if not args.dryRun:
                subprocess.run(
                    f"docker pull {fromPkg}", shell=True, check=True,
                )
                subprocess.run(
                    f"docker tag {fromPkg} {toPkg}", shell=True, check=True,
                )
                subprocess.run(
                    f"docker push {toPkg}", shell=True, check=True,
                )


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description="Migrates package docker images from one docker org to another one."
    )
    parser.add_argument("--from", "-f", dest="fromOrg", default="aswftesting")
    parser.add_argument("--to", "-t", dest="toOrg", default="aswf")
    parser.add_argument("--dry-run", "-d", dest="dryRun", action="store_true")
    args = parser.parse_args()
    migrate(args)


if __name__ == "__main__":
    main()
