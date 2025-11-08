#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir rawtoaces
cd rawtoaces

if [ ! -f "$DOWNLOADS_DIR/rawtoaces-${ASWF_RAWTOACES_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/AcademySoftwareFoundation/rawtoaces/archive/refs/tags/v${ASWF_RAWTOACES_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/rawtoaces-${ASWF_RAWTOACES_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/rawtoaces-${ASWF_RAWTOACES_VERSION}.tar.gz"
cd "rawtoaces-${ASWF_RAWTOACES_VERSION}"

mkdir build
cd build
cmake \
     -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
     ..
cmake --build . -j$(nproc)
cmake --install .

cd ../../..
rm -rf rawtoaces
