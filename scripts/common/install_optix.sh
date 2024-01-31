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

# Optix SDK 7.0.0 does not have include package, download include files directly.

OptiXDirs_70=( "include" "include/internal" "include/optixPaging" )
OptiXHeaders_70=( \
"internal/optix_7_device_impl.h" \
"internal/optix_7_device_impl_exception.h" \
"internal/optix_7_device_impl_transformations.h" \
"optixPaging/optixPaging.cu" \
"optixPaging/optixPaging.h" \
"optixPaging/optixPagingImpl.cpp" \
"optix.h" \
"optix_7_device.h" \
"optix_7_host.h" \
"optix_7_types.h" \
"optix_device.h" \
"optix_function_table.h" \
"optix_function_table_definition.h" \
"optix_host.h" \
"optix_stack_size.h" \
"optix_stubs.h" \
"optix_types.h")

OPTIX_VERSION=7.0
OPTIXLOC=https://developer.download.nvidia.com/redist/optix/v${OPTIX_VERSION}
for d in ${OptiXDirs_70[@]}
do
    mkdir -p $OPTIX_SDK_PREFIX-$OPTIX_VERSION.0/$d
done
for f in ${OptiXHeaders_70[@]}
do
    curl --retry 100 -m 120 --connect-timeout 30 \
        $OPTIXLOC/include/$f > $OPTIX_SDK_PREFIX-$OPTIX_VERSION.0/include/$f
done

# No known open downloads for 7.1.0 or 7.2.0


# Zip files for 7.3.0 and newer, with some variability in ZIP filename and directory prefix

declare -A OPTIX_VERSION_ZIP=( [7.3]=7.3.0 [7.4]=7.4.0 [7.5]=7.5 [7.6]=7.6 [7.7]=7.7 [8.0]=8.0 )
declare -A OPTIX_VERSION_DIR=( [7.3]="" [7.4]="" [7.5]="include" [7.6]="include" [7.7]="include" [8.0]="include" )

for OPTIX_VERSION in 7.3 7.4 7.5 7.6 7.7 8.0
do
    OPTIXLOC=https://developer.download.nvidia.com/redist/optix/v${OPTIX_VERSION}
    curl --retry 100 -m 120 --connect-timeout 30 \
        -o /tmp/OptiX-${OPTIX_VERSION}-Include.zip $OPTIXLOC/OptiX-${OPTIX_VERSION_ZIP[$OPTIX_VERSION]}-Include.zip
    # Not all zip files are structured the same
    OPTIX_INSTALL_DIR=$OPTIX_SDK_PREFIX-$OPTIX_VERSION.0/${OPTIX_VERSION_DIR[$OPTIX_VERSION]}/
    mkdir -p $OPTIX_INSTALL_DIR
    unzip -d $OPTIX_INSTALL_DIR /tmp/OptiX-${OPTIX_VERSION}-Include.zip
done

