#!/usr/bin/env bash
set -ex

image_name=${1}
image_version=${2}
repo_uri=${3:-""}
repo_branch=${4:-""}

if [ "$repo_branch" = "refs/heads/master" ] && [ "$repo_uri" = "https://github.com/AcademySoftwareFoundation/aswf-docker" ]
then
    docker_build_date=`date -u +'%Y-%m-%dT%H:%M:%SZ'`
    docker_vcs_ref=`git rev-parse --short HEAD`
    docker_org=aswf
    packages_docker_org=aswf
    push_images=true
elif [ "$repo_branch" = "refs/heads/testing" ]
then
    docker_build_date=`date -u +'%Y-%m-%dT%H:%M:%SZ'`
    docker_vcs_ref=`git rev-parse --short HEAD`
    docker_org=aswftesting
    packages_docker_org=aswftesting
    push_images=true
else
    docker_build_date=dev
    docker_vcs_ref=dev
    docker_org=aswflocaltesting # this org is not valid, but this ensures that the test will not accidently pull an existing image
    packages_docker_org=aswftesting
    push_images=false
fi

# Replace aswftesting with aswf (https://github.com/docker/buildx/issues/148 should allow this hack to be removed)
if [ "${docker_org}" != "aswftesting" ]
then
    sed -i --expression="s/aswftesting/${docker_org}/g" docker-bake-${image_name}-${image_version}.hcl
fi

# Configure docker arguments depending if push is required
BUILDX_ARGS="-f docker-bake-settings.hcl \
    -f docker-bake-${image_name}-${image_version}.hcl \
    --set settings.args.ASWF_ORG=${packages_docker_org}"

if [ "${push_images}" = "true" ]
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
