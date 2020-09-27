#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/partio-${PARTIO_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/wdas/partio/archive/v${PARTIO_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/partio-${PARTIO_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/partio-${PARTIO_VERSION}.tar.gz"
cd "partio-${PARTIO_VERSION}"

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" ..
make -j$(nproc)
make install

cd ../..
rm -rf "partio-${PARTIO_VERSION}"
