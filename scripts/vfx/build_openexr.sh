#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f $DOWNLOADS_DIR/openexr-${OPENEXR_VERSION}.tar.gz ]; then
    curl --location https://github.com/AcademySoftwareFoundation/openexr/archive/v${OPENEXR_VERSION}.tar.gz -o $DOWNLOADS_DIR/openexr-${OPENEXR_VERSION}.tar.gz
fi

tar xf $DOWNLOADS_DIR/openexr-${OPENEXR_VERSION}.tar.gz
cd openexr-${OPENEXR_VERSION}

if [[ $OPENEXR_VERSION == 2.2* ]]; then

    cd IlmBase
    ./bootstrap
    ./configure --prefix=${ASWF_INSTALL_PREFIX}
    make -j$(nproc)
    make install

    cd ../OpenEXR
    ./bootstrap
    ./configure --prefix=${ASWF_INSTALL_PREFIX}
    make -j$(nproc)
    make install

    cd ../PyIlmBase
    ./bootstrap
    ./configure --prefix=${ASWF_INSTALL_PREFIX}
    make
    make install
else

    # TODO: add support for python-3 PyIlmBase when it works...
    if [[ $OPENEXR_VERSION == 2.3.0 ]]; then
        if [[ $PYTHON_VERSION == 2.7* ]]; then
            BUILD_PYILMBASE=on
        else
            BUILD_PYILMBASE=off
        fi
    else
        BUILD_PYILMBASE=on
    fi

    mkdir build
    cd build
    cmake \
        -DCMAKE_INSTALL_PREFIX=${ASWF_INSTALL_PREFIX} \
        -DOPENEXR_BUILD_PYTHON_LIBS=${BUILD_PYILMBASE} \
        ..
    make -j$(nproc)
    make install
fi

cd ../..
rm -rf openexr-${OPENEXR_VERSION}
