#!/usr/bin/env bash
set -ex

group_name=${1}
group_version=${2}
push_packages=${3}
repo_uri=${4}
repo_branch=${5}

if [ "$repo_branch" = "refs/heads/master" ] && [ "$repo_uri" = "https://github.com/AcademySoftwareFoundation/aswf-docker" ]
then
    docker_build_date=`date -u +'%Y-%m-%dT%H:%M:%SZ'`
    docker_vcs_ref=`git rev-parse --short HEAD`
    docker_org=aswf
elif [ "$repo_branch" = "refs/heads/testing" ]
then
    docker_build_date=`date -u +'%Y-%m-%dT%H:%M:%SZ'`
    docker_vcs_ref=`git rev-parse --short HEAD`
    docker_org=aswftesting
else
    docker_build_date=dev
    docker_vcs_ref=dev
    docker_org=aswftesting
fi

# Replace aswftesting with aswf (https://github.com/docker/buildx/issues/148 should allow this hack to be removed)
if [ "${docker_org}" = "aswf" ]
then
    sed -i --expression="s/aswftesting/aswf/g" packages/docker-bake-${group_name}-${group_version}.hcl
fi

BUILDX_ARGS="-f docker-bake-settings.hcl \
    -f packages/docker-bake-packages-${group_name}-${group_version}.hcl \
    --set settings.args.ASWF_ORG=${docker_org}"

if [ "${push_packages}" = "true" ]
then
    BUILDX_ARGS="${BUILDX_ARGS} \
        --set settings.args.BUILD_DATE=${docker_build_date} \
        --set settings.args.VCS_REF=${docker_vcs_ref} \
        --set settings.output=type=registry,push=true"
else
    BUILDX_ARGS="${BUILDX_ARGS} \
        --set settings.output=type=docker"
fi

docker buildx bake ${BUILDX_ARGS}
