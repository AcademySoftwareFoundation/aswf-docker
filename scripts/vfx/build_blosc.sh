#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

git clone https://github.com/Blosc/c-blosc.git
cd c-blosc

if [ "$ASWF_BLOSC_VERSION" != "latest" ]; then
    git checkout "tags/v${ASWF_BLOSC_VERSION}" -b "v${ASWF_BLOSC_VERSION}"
fi

mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}"
make -j$(nproc)
make install

cd ../..
rm -rf c-blosc
