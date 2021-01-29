#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/pybind11-${ASWF_PYBIND11_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/pybind/pybind11/archive/v${ASWF_PYBIND11_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/pybind11-${ASWF_PYBIND11_VERSION}.tar.gz"
fi
tar -zxf "$DOWNLOADS_DIR/pybind11-${ASWF_PYBIND11_VERSION}.tar.gz"
cd "pybind11-${ASWF_PYBIND11_VERSION}"

mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" ..
make -j$(nproc)
make install

cd ../..

rm -rf "pybind11-${ASWF_PYBIND11_VERSION}"
