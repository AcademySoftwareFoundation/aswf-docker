#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/archive/refs/tags/v${ASWF_OSL_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz"
cd "OpenShadingLanguage-${ASWF_OSL_VERSION}"

if [[ $ASWF_DTS_VERSION == 9 && $ASWF_CUDA_VERSION == 10* ]]; then
    CUDA_COMPUTE_VERSION=compute_30
else
    CUDA_COMPUTE_VERSION=compute_50
fi

mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
      -DBoost_USE_STATIC_LIBS=OFF \
      -DBUILD_SHARED_LIBS=ON \
      -DCMAKE_CXX_STANDARD=$ASWF_CXX_STANDARD \
      -Dpybind11_DIR="${ASWF_INSTALL_PREFIX}/lib/cmake/pybind11" \
      -DOSL_USE_OPTIX=ON \
      -DOPTIX_VERSION=${ASWF_OPTIX_VERSION} \
      -DOPTIXHOME=${ASWF_INSTALL_PREFIX}/NVIDIA-OptiX-SDK-${ASWF_OPTIX_VERSION} \
      ../.

cmake --build . -j$(nproc) --verbose
cmake --install .

cd ../..
rm -rf "OpenShadingLanguage-${ASWF_OSL_VERSION}"
