#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/osl-${OSL_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/imageworks/OpenShadingLanguage/archive/Release-${OSL_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/osl-${OSL_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/osl-${OSL_VERSION}.tar.gz"
cd "OpenShadingLanguage-Release-${OSL_VERSION}"

mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
      -DBoost_USE_STATIC_LIBS=OFF \
      -DBUILD_SHARED_LIBS=ON \
      -DCMAKE_CXX_STANDARD=14 \
      ../.

make -j$(nproc)
make install

cd ../..
rm -rf "OpenShadingLanguage-Release-${OSL_VERSION}"
