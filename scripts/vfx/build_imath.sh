#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [[ $ASWF_IMATH_VERSION == 2* ]]; then
    echo "Imath package is a dummy package with no actual file for v2."
    touch ${ASWF_INSTALL_PREFIX}/no-imath-${ASWF_IMATH_VERSION}-package
else
    if [ ! -f "$DOWNLOADS_DIR/Imath-${ASWF_IMATH_VERSION}.tar.gz" ]; then
        curl --location "https://github.com/AcademySoftwareFoundation/Imath/archive/v${ASWF_IMATH_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/Imath-${ASWF_IMATH_VERSION}.tar.gz"
    fi

    tar xf "$DOWNLOADS_DIR/Imath-${ASWF_IMATH_VERSION}.tar.gz"
    cd "Imath-${ASWF_IMATH_VERSION}"

    mkdir build
    cd build
    cmake \
        -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
        -DPYTHON=ON \
        ..
    make -j$(nproc)
    make install

    cd ../..
    rm -rf $IMATH_FOLDER
fi

