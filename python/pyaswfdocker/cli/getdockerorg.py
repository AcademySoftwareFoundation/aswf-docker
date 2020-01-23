#!/usr/bin/env python3

import argparse
from .. import utils


def main():
    parser = argparse.ArgumentParser(
        description="Outputs the docker organisation to use according to the inputs"
    )
    parser.add_argument("--repo-uri", "-r")
    parser.add_argument("--source-branch", "-b")
    args = parser.parse_args()
    print(utils.get_docker_org(args.repo_uri, args.source_branch))


if __name__ == "__main__":
    main()
