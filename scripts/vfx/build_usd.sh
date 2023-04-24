#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

pip install jinja2 PyOpenGL

if [ ! -f "$DOWNLOADS_DIR/usd-${ASWF_USD_VERSION}.tar.gz" ]; then
     curl --location "https://github.com/PixarAnimationStudios/USD/archive/v${ASWF_USD_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/usd-${ASWF_USD_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/usd-${ASWF_USD_VERSION}.tar.gz"
cd "USD-${ASWF_USD_VERSION}"

if [[ $ASWF_USD_VERSION == 23.05 && $ASWF_MATERIALX_VERSION == 1.38.7 ]]; then
    # Apply patch from https://github.com/PixarAnimationStudios/USD/pull/2402
    curl --location "https://patch-diff.githubusercontent.com/raw/PixarAnimationStudios/USD/pull/2402.diff" | patch -p1
fi 

if [[ $ASWF_USD_VERSION == 19.* ]]; then
     VT_SRC_FOLDER=base/lib/vt
else
     VT_SRC_FOLDER=base/vt
fi

mkdir build
cd build

if [[ $ASWF_PYTHON_VERSION == 2.7* ]]; then
    USD_EXTRA_ARGS=
else
    USD_EXTRA_ARGS=-DPXR_USE_PYTHON_3=ON
fi

cmake \
     -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
     -DOPENEXR_LOCATION="${ASWF_INSTALL_PREFIX}" \
     -DCPPUNIT_LOCATION="${ASWF_INSTALL_PREFIX}" \
     -DBLOSC_LOCATION="${ASWF_INSTALL_PREFIX}" \
     -DTBB_LOCATION="${ASWF_INSTALL_PREFIX}" \
     -DILMBASE_LOCATION="${ASWF_INSTALL_PREFIX}" \
     -DGLEW_LOCATION="${ASWF_INSTALL_PREFIX}" \
     -DMATERIALX_LOCATION="${ASWF_INSTALL_PREFIX}" \
     -DPXR_ENABLE_MATERIALX_SUPPORT=ON \
     -DPXR_BUILD_TESTS=OFF \
     -DUSD_ROOT_DIR="${ASWF_INSTALL_PREFIX}" \
     -DPXR_BUILD_ALEMBIC_PLUGIN=OFF \
     -DPXR_BUILD_MAYA_PLUGIN=FALSE \
     ${USD_EXTRA_ARGS} \
     ..

make -j$(nproc)
make install

cd ../..

rm -rf "USD-${ASWF_USD_VERSION}"
