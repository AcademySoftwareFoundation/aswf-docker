#!/usr/bin/env bash
set -ex

repo_uri=${1:-""}
repo_branch=${2:-""}

if [ "$repo_branch" = refs/heads/master ] && [ "$repo_uri" = https://github.com/AcademySoftwareFoundation/aswf-docker ]
then
    docker_org=aswf
elif [ "$repo_branch" = refs/heads/testing ]
then
    docker_org=aswftesting
else
    docker_org=aswflocaltesting # this org is not valid, but this ensures that the test will not accidently pull an existing image
fi

export DOCKER_ORG=${docker_org}
