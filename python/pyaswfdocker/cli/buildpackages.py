#!/usr/bin/env python3

import logging
import argparse

from pyaswfdocker import builder, buildinfo

logger = logging.getLogger("build-packages")


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="Builds docker packages")
    parser.add_argument("--repo-uri", "-r")
    parser.add_argument("--source-branch", "-b")
    parser.add_argument("--group-name", "-n", dest="groupName")
    parser.add_argument("--group-version", "-v", dest="groupVersion")
    parser.add_argument("--push", "-p", action="store_true")
    parser.add_argument("--dry-run", "-d", action="store_true", dest="dryRun")
    args = parser.parse_args()
    b = builder.Builder(
        buildinfo.BuildInfo(dockerOrg=args.dockerOrg),
        dryRun=args.dryRun,
        groupName=args.groupName,
        groupVersion=args.groupVersion,
        push=args.push,
    )
    b.build()


if __name__ == "__main__":
    main()
