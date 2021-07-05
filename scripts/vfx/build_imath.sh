#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [[ $ASWF_IMATH_VERSION == 2* ]]; then
    IMATH_URL="https://github.com/AcademySoftwareFoundation/OpenEXR/archive/v${ASWF_IMATH_VERSION}.tar.gz"
    IMATH_FOLDER="openexr-${ASWF_IMATH_VERSION}"
else
    IMATH_URL="https://github.com/AcademySoftwareFoundation/Imath/archive/v${ASWF_IMATH_VERSION}.tar.gz"
    IMATH_FOLDER="Imath-${ASWF_IMATH_VERSION}"
fi

if [ ! -f "$DOWNLOADS_DIR/Imath-${ASWF_IMATH_VERSION}.tar.gz" ]; then
    curl --location $IMATH_URL -o "$DOWNLOADS_DIR/Imath-${ASWF_IMATH_VERSION}.tar.gz"
fi

tar xf "$DOWNLOADS_DIR/Imath-${ASWF_IMATH_VERSION}.tar.gz"
cd $IMATH_FOLDER

if [[ $ASWF_IMATH_VERSION == 2.2* ]]; then

    cd IlmBase
    ./bootstrap
    ./configure --prefix="${ASWF_INSTALL_PREFIX}"
    make -j$(nproc)
    make install

    cd ../PyIlmBase
    ./bootstrap
    ./configure --prefix="${ASWF_INSTALL_PREFIX}"
    make
    make install

elif [[ $ASWF_IMATH_VERSION == 2* ]]; then

    mkdir b1
    cd b1
    cmake \
        -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
        ../IlmBase
    make -j$(nproc)
    make install
    cd ..

    mkdir b2
    cd b2
    cmake \
        -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
        -DIMATH_BUILD_PYTHON_LIBS=ON \
        -DBUILD_SHARED_LIBS=ON \
        ../PyIlmBase
    make -j$(nproc)
    make install

else
    mkdir build
    cd build
    cmake \
        -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
        -DPYTHON=ON \
        ..
    make -j$(nproc)
    make install
fi

cd ../..
rm -rf $IMATH_FOLDER
