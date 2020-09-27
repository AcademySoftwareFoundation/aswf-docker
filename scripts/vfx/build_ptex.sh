#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir ptex
cd ptex

if [ $PTEX_VERSION = "2.3.2" ]; then
    # Need to use a commit that is later than the official 2.3.2 release and fixes a cmake issue when outside of git
    PTEX_TAG="24bb5de40383f177cb1a7886fba4c8398ba4c22e"
else
    PTEX_TAG="v${PTEX_VERSION}"
fi

if [ ! -f "$DOWNLOADS_DIR/ptex-${PTEX_VERSION}.tar.gz" ]; then
    curl --location "http://github.com/wdas/ptex/archive/${PTEX_TAG}.tar.gz" -o "$DOWNLOADS_DIR/ptex-${PTEX_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/ptex-${PTEX_VERSION}.tar.gz"

if [ $PTEX_VERSION = "2.3.2" ]; then
    # rename folder to expected name
    mv "ptex-${PTEX_TAG}" "ptex-${PTEX_VERSION}"
fi

cd "ptex-${PTEX_VERSION}"
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" ..
make -j$(nproc)
make install

cd ../../..
rm -rf ptex
