#!/usr/bin/env python3

import logging
import argparse
import subprocess
import json

from .. import builder

logger = logging.getLogger("build-packages")


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="Builds docker packages")
    parser.add_argument("--docker-org", "-o", dest="dockerOrg")
    parser.add_argument("--group-name", "-n", dest="groupName")
    parser.add_argument("--group-version", "-v", dest="groupVersion")
    parser.add_argument("--push", "-p", action="store_true")
    parser.add_argument("--dry-run", "-d", action="store_true", dest="dryRun")
    args = parser.parse_args()
    b = builder.Builder(
        dryRun=args.dryRun,
        groupName=args.groupName,
        groupVersion=args.groupVersion,
        push=args.push,
        dockerOrg=args.dockerOrg,
    )
    b.build()


if __name__ == "__main__":
    main()
