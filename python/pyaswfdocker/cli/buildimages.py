#!/usr/bin/env python3

import logging
import argparse

from .. import builder, buildinfo

logger = logging.getLogger("build-images")


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="Builds docker images")
    parser.add_argument("--repo-uri", "-r")
    parser.add_argument("--source-branch", "-b")
    parser.add_argument("--image-type", "-i")
    parser.add_argument("--group-name", "-g")
    parser.add_argument("--group-version", "-v")
    parser.add_argument("--target", "-t")
    parser.add_argument("--push", "-p", action="store_true")
    parser.add_argument("--dry-run", "-d", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--aswf-version")
    args = parser.parse_args()
    b = builder.Builder(
        buildinfo.BuildInfo(repoUri=args.repo_uri, sourceBranch=args.source_branch, aswfVersion=args.aswf_version),
        dryRun=args.dry_run,
        groupName=args.group_name,
        groupVersion=args.group_version,
        push=args.push,
        imageType=args.image_type,
        target=args.target,
        verbose=args.verbose,
    )
    b.build()


if __name__ == "__main__":
    main()
