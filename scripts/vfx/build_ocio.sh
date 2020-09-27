#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir ocio
cd ocio


if [ ! -f "$DOWNLOADS_DIR/ocio-${OCIO_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/v${OCIO_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/ocio-${OCIO_VERSION}.tar.gz"
fi
tar -zxf "$DOWNLOADS_DIR/ocio-${OCIO_VERSION}.tar.gz"
cd "OpenColorIO-${OCIO_VERSION}"

if [[ $DTS_VERSION == 9 && $OCIO_VERSION == 1.* ]]; then
    # Disable warning treated as errors
    sed -i 's/-Werror//g' src/core/CMakeLists.txt
    sed -i 's/-Werror//g' src/pyglue/CMakeLists.txt
fi

mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
    -DOCIO_BUILD_STATIC=OFF \
    -DOCIO_BUILD_TRUELIGHT=OFF \
    -DOCIO_BUILD_APPS=OFF \
    -DOCIO_BUILD_NUKE=OFF \
    -DCMAKE_CXX_FLAGS="-Wno-error=unused-function -Wno-error=deprecated-declarations"\
    ..
make -j$(nproc)
make install

cd ../..

curl --location "https://github.com/imageworks/OpenColorIO-Configs/archive/v${OCIO_CONFIGS_VERSION}.tar.gz" -o "ocio-configs.tar.gz"
tar -zxf ocio-configs.tar.gz
cd "OpenColorIO-Configs-${OCIO_CONFIGS_VERSION}"

mkdir "${ASWF_INSTALL_PREFIX}/openColorIO"
cp nuke-default/config.ocio "${ASWF_INSTALL_PREFIX}/openColorIO/"
cp -r nuke-default/luts "${ASWF_INSTALL_PREFIX}/openColorIO/"

cd ../..
rm -rf ocio
