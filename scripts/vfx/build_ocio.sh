#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir ocio
cd ocio

if [ ! -f "$DOWNLOADS_DIR/ocio-${ASWF_OCIO_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/v${ASWF_OCIO_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/ocio-${ASWF_OCIO_VERSION}.tar.gz"
fi
tar -zxf "$DOWNLOADS_DIR/ocio-${ASWF_OCIO_VERSION}.tar.gz"
cd "OpenColorIO-${ASWF_OCIO_VERSION}"


if [[ $ASWF_DTS_VERSION == 9 && $ASWF_OCIO_VERSION == 1.* ]]; then
    # Disable warning treated as errors
    sed -i 's/-Werror//g' src/core/CMakeLists.txt
    sed -i 's/-Werror//g' src/pyglue/CMakeLists.txt
fi

mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
    -DOCIO_USE_OIIO_FOR_APPS=OFF \
    -DOCIO_BUILD_STATIC=OFF \
    -DOCIO_BUILD_TRUELIGHT=OFF \
    -DOCIO_BUILD_APPS=OFF \
    -DOCIO_BUILD_NUKE=OFF \
    -DOCIO_INSTALL_EXT_PACKAGES=MISSING \
    -Dpybind11_ROOT="${ASWF_INSTALL_PREFIX}" \
    -DGLEW_ROOT="${ASWF_INSTALL_PREFIX}" \
    -DCMAKE_CXX_FLAGS="-Wno-error=unused-function -Wno-error=deprecated-declarations"\
    ..
make -j$(nproc)
make install

cd ../..

curl --location "https://github.com/imageworks/OpenColorIO-Configs/archive/v${ASWF_OCIO_CONFIGS_VERSION}.tar.gz" -o "ocio-configs.tar.gz"
tar -zxf ocio-configs.tar.gz
cd "OpenColorIO-Configs-${ASWF_OCIO_CONFIGS_VERSION}"

mkdir "${ASWF_INSTALL_PREFIX}/openColorIO"
cp nuke-default/config.ocio "${ASWF_INSTALL_PREFIX}/openColorIO/"
cp -r nuke-default/luts "${ASWF_INSTALL_PREFIX}/openColorIO/"

cd ../..
rm -rf ocio
