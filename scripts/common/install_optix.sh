#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Download and install the NVIDIA Optix includes. The full NVIDIA Optix SDK
# requires a developer account to download, but only the include files are required
# to build and some of the SDK includes can be accessed directly.
#
# The FindOptix.cmake module can be found here: https://github.com/NVIDIA/otk-cmake
#
# The Optix SDK version is currently not specified by the VFX Reference Platform,
# we install all available header versions in /usr/local/NVIDIA-OptiX-SDK-7.x.x/include/
# and let the project set the Cmake variable Optix_ROOT_DIR to pick the version it needs.

set -ex

OPTIX_SDK_PREFIX=/usr/local/NVIDIA-OptiX-SDK

for OPTIX_VERSION in 7.0.0 7.1.0 7.2.0 7.3.0 7.4.0 7.5.0 7.6.0 7.7.0 8.0.0 8.1.0 9.0.0
do
    OPTIXLOC=https://github.com/NVIDIA/optix-dev/archive/refs/tags/v${OPTIX_VERSION}.tar.gz
    OPTIX_INSTALL_DIR=${OPTIX_SDK_PREFIX}-${OPTIX_VERSION}/include
    mkdir -p $OPTIX_INSTALL_DIR
    curl --retry 100 -m 120 --connect-timeout 30 \
        -sL $OPTIXLOC | (cd ${OPTIX_INSTALL_DIR} ; tar --strip-components=2 -x -z -f - optix-dev-${OPTIX_VERSION}/include )
done

