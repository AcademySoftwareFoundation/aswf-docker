#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

pip3 install jinja2 PyOpenGL

if [[ ! -f "$DOWNLOADS_DIR/usd-${ASWF_OPENUSD_VERSION}.tar.gz" ]]; then
    # For VFX Platform 2025, we need a somewhat newer release of USD than the latest 25.05a tag to
    # get MaterialX 1.39.3 compatibility.
    if [[ $ASWF_OPENUSD_VERSION == 25.02a.eae7e67 ]]; then
        curl --location "https://github.com/PixarAnimationStudios/OpenUSD/archive/eae7e678473eb78794a3a27287ff121af322d583.tar.gz" -o "$DOWNLOADS_DIR/usd-${ASWF_OPENUSD_VERSION}.tar.gz"
    else
        curl --location "https://github.com/PixarAnimationStudios/OpenUSD/archive/v${ASWF_OPENUSD_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/usd-${ASWF_OPENUSD_VERSION}.tar.gz"
    fi
fi

tar -zxf "$DOWNLOADS_DIR/usd-${ASWF_OPENUSD_VERSION}.tar.gz"
cd "OpenUSD-${ASWF_OPENUSD_VERSION}"

if [[ $ASWF_OPENUSD_VERSION == 23.05 && $ASWF_MATERIALX_VERSION == 1.38.7 ]]; then
    # Apply patch from https://github.com/PixarAnimationStudios/USD/pull/2402
    curl --location "https://patch-diff.githubusercontent.com/raw/PixarAnimationStudios/USD/pull/2402.diff" | patch -p1
fi 

if [[ $ASWF_OPENUSD_VERSION == 24.08 && $ASWF_MATERIALX_VERSION == 1.39.1 ]]; then
    # Apply patch from https://github.com/PixarAnimationStudios/USD/pull/3159
    curl --location "https://patch-diff.githubusercontent.com/raw/PixarAnimationStudios/OpenUSD/pull/3159.diff" | patch -p1
fi

mkdir build
cd build

cmake \
     -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
     -DPXR_BUILD_ALEMBIC_PLUGIN=ON \
     -DPXR_ENABLE_HDF5_SUPPORT=ON \
     -DPXR_BUILD_GPU_SUPPORT=ON \
     -DPXR_ENABLE_GL_SUPPORT=ON \
     -DPXR_ENABLE_METAL_SUPPORT=OFF \
     -DPXR_ENABLE_VULKAN_SUPPORT=OFF \
     -DMATERIALX_STDLIB_DIR="${ASWF_INSTALL_PREFIX}/share/MaterialX" \
     -DPXR_ENABLE_MATERIALX_SUPPORT=ON \
     -DPXR_BUILD_OPENCOLORIO_PLUGIN=ON \
     -DPXR_BUILD_OPENIMAGEIO_PLUGIN=ON \
     -DPXR_ENABLE_OPENVDB_SUPPORT=ON \
     -DPXR_ENABLE_OSL_SUPPORT=ON \
     -DPXR_ENABLE_PTEX_SUPPORT=ON \
     -DPXR_ENABLE_PYTHON_SUPPORT=ON \
     -DPXR_BUILD_TESTS=OFF \
     -DUSD_ROOT_DIR="${ASWF_INSTALL_PREFIX}" \
     -DPXR_BUILD_MAYA_PLUGIN=FALSE \
     -DPXR_BUILD_USDVIEW=ON \
     -DPYSIDEUICBINARY="${ASWF_INSTALL_PREFIX}/bin/uic" \
     ${USD_EXTRA_ARGS} \
     ..
cmake --build . -j$(nproc)
cmake --install .

cd ../..

rm -rf "OpenUSD-${ASWF_OPENUSD_VERSION}"
