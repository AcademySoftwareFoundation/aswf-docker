#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/openexr-${ASWF_OPENEXR_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/AcademySoftwareFoundation/openexr/archive/v${ASWF_OPENEXR_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/openexr-${ASWF_OPENEXR_VERSION}.tar.gz"
fi

tar xf "$DOWNLOADS_DIR/openexr-${ASWF_OPENEXR_VERSION}.tar.gz"
cd "openexr-${ASWF_OPENEXR_VERSION}"

if [[ $ASWF_OPENEXR_VERSION == 2.2* ]]; then

    cd ../OpenEXR
    ./bootstrap
    ./configure --prefix="${ASWF_INSTALL_PREFIX}"
    make -j$(nproc)
    make install

elif [[ $ASWF_IMATH_VERSION == 2* ]]; then

    if [[ $ASWF_OPENEXR_VERSION == 2.3.0 ]]; then
        if [[ $ASWF_PYTHON_VERSION == 2.7* ]]; then
            BUILD_PYTHON_LIBS=on
        else
            BUILD_PYTHON_LIBS=off
        fi
    else
        BUILD_PYTHON_LIBS=on
    fi

    mkdir build
    cd build
    cmake \
        -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
        -DOPENEXR_BUILD_PYTHON_LIBS="${BUILD_PYTHON_LIBS}" \
        ../OpenEXR
    make -j$(nproc)
    make install

else

    mkdir build
    cd build
    cmake \
        -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
        -DOPENEXR_BUILD_PYTHON_LIBS=ON \
        ..
    make -j$(nproc)
    make install

fi

cd ../..
rm -rf "openexr-${ASWF_OPENEXR_VERSION}"
