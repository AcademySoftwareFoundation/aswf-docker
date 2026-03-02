#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir rawtoaces
cd rawtoaces

ASWF_RAWTOACES_VERSION_DOWNLOAD=${ASWF_RAWTOACES_VERSION}
if [[ ${ASWF_RAWTOACES_VERSION_DOWNLOAD} == 1.1.0 ]]; then
    # asset name doesn't match version
    ASWF_RAWTOACES_VERSION_DOWNLOAD=1.1
fi

if [ ! -f "$DOWNLOADS_DIR/rawtoaces-${ASWF_RAWTOACES_VERSION_DOWNLOAD}.tar.gz" ]; then
    curl --location "https://github.com/AcademySoftwareFoundation/rawtoaces/archive/refs/tags/v${ASWF_RAWTOACES_VERSION_DOWNLOAD}.tar.gz" -o "$DOWNLOADS_DIR/rawtoaces-${ASWF_RAWTOACES_VERSION_DOWNLOAD}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/rawtoaces-${ASWF_RAWTOACES_VERSION_DOWNLOAD}.tar.gz"
cd "rawtoaces-${ASWF_RAWTOACES_VERSION_DOWNLOAD}"

mkdir build
cd build
cmake \
     -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
     -DRTA_BUILD_PYTHON_BINDINGS=FALSE \
     ..
cmake --build . -j$(nproc)
cmake --install .

cd ../../..
rm -rf rawtoaces
