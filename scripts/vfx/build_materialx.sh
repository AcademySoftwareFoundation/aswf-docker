#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir materialx
cd materialx

if [ ! -f "$DOWNLOADS_DIR/materialx-${ASWF_MATERIALX_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/AcademySoftwareFoundation/MaterialX/archive/v${ASWF_MATERIALX_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/materialx-${ASWF_MATERIALX_VERSION}.tar.gz"
fi
tar -zxf "$DOWNLOADS_DIR/materialx-${ASWF_MATERIALX_VERSION}.tar.gz"
cd "MaterialX-${ASWF_MATERIALX_VERSION}"

mkdir build
cd build
# Can't enable MATERIALX_BUILD_VIEWER until we provide NanoGUI
# Can't enable MATERIALX_BUILD_GRAPH_EDITOR until we provide ImGUI
cmake \
    -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
    -DMATERIALX_BUILD_PYTHON=ON \
    -DMATERIALX_BUILD_VIEWER=OFF \
    -DMATERIALX_BUILD_GRAPH_EDITOR=OFF \
    -DMATERIALX_BUILD_SHARED_LIBS=ON \
    -DMATERIALX_BUILD_OIIO=ON \
    -DMATERIALX_BUILD_OCIO=ON \
    ..
cmake --build . -j$(nproc)
cmake --install .

cd ../..
rm -rf materialx
