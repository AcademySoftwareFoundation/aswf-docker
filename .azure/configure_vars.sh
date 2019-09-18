#!/bin/sh

# This script outputs variables to be processed by the Azure Pipeline

set -ex

echo "Repo URI: $1"
echo "Branch: $2"

if [ $2 = refs/heads/master ] && [ $1 = https://github.com/AcademySoftwareFoundation/aswf-docker ]
then
    docker_build_date=`date -u +'%Y-%m-%dT%H:%M:%SZ'`
    docker_vcs_ref=`git rev-parse --short HEAD`
    docker_org=aswf
    push_images=true
elif [ $2 = refs/heads/testing ]
then
    docker_build_date=`date -u +'%Y-%m-%dT%H:%M:%SZ'`
    docker_vcs_ref=`git rev-parse --short HEAD`
    docker_org=aswftesting
    push_images=true
else
    docker_build_date=dev
    docker_vcs_ref=dev
    docker_org=aswftesting
    push_images=false
fi

# Output variables for current job
echo "##vso[task.setvariable variable=docker_build_date]${docker_build_date}"
echo "##vso[task.setvariable variable=docker_vcs_ref]${docker_vcs_ref}"
echo "##vso[task.setvariable variable=docker_org]${docker_org}"
echo "##vso[task.setvariable variable=push_images]${push_images}"

# Output variables for downstream jobs
echo "##vso[task.setvariable variable=docker_build_date;isOutput=true]${docker_build_date}"
echo "##vso[task.setvariable variable=docker_vcs_ref;isOutput=true]${docker_vcs_ref}"
echo "##vso[task.setvariable variable=docker_org;isOutput=true]${docker_org}"
echo "##vso[task.setvariable variable=push_images;isOutput=true]${push_images}"
