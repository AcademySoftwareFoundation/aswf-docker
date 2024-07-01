#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/archive/refs/tags/v${ASWF_OSL_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz"
cd "OpenShadingLanguage-${ASWF_OSL_VERSION}"

export PUGIXML_INSTALL_DIR=${ASWF_INSTALL_PREFIX}
if [[ ! $ASWF_OSL_VERSION == 1.10* ]]; then
    src/build-scripts/build_pugixml.bash
fi

mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
      -DBoost_USE_STATIC_LIBS=OFF \
      -DBUILD_SHARED_LIBS=ON \
      -DCMAKE_CXX_STANDARD="${ASWF_CXX_STANDARD}" \
      ../.

make -j$(nproc)
make install

cd ../..
rm -rf "OpenShadingLanguage-Release-${ASWF_OSL_VERSION}"
