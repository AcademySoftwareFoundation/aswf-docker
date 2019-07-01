#!/usr/bin/env bash

set -ex

ASWF_ORG=${DOCKERHUB_ORG:-aswfstaging}
CI_COMMON_VERSION=${CI_COMMON_VERSION:-1.0}
VFXPLATFORM_VERSION=${VFXPLATFORM_VERSION:-2019}
ASWF_VERSION=${ASWF_VERSION:-${VFXPLATFORM_VERSION}}
BUILD_DATE=${BUILD_DATE:-dev}
VCS_REF=${VCS_REF:-dev}

# Also source versions environment variables here as docker image needs some as build arguments
# Exemple: PYTHON_VERSION
source scripts/${VFXPLATFORM_VERSION}/versions_base.sh

BUILD_ARGS=" --build-arg BUILD_DATE=${BUILD_DATE} \
             --build-arg ASWF_ORG=${ASWF_ORG} \
             --build-arg VFXPLATFORM_VERSION=${VFXPLATFORM_VERSION} \
             --build-arg CI_COMMON_VERSION=${CI_COMMON_VERSION} \
             --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
             --build-arg VCS_REF=${VCS_REF}"

docker build -t ${ASWF_ORG}/ci-base:${ASWF_VERSION} -f ci-base/Dockerfile ${BUILD_ARGS} .

# Most VFX packages are not ready for python3 yet...
if [[ ${VFXPLATFORM_VERSION} != 2020 ]]; then
    docker build -t ${ASWF_ORG}/ci-ocio:${ASWF_VERSION} -f ci-ocio/Dockerfile ${BUILD_ARGS} .
    docker build -t ${ASWF_ORG}/ci-openvdb:${ASWF_VERSION} -f ci-openvdb/Dockerfile ${BUILD_ARGS} .
fi
