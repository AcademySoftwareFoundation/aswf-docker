#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir ccache
cd ccache

if [ ! -f "$DOWNLOADS_DIR/ccache-${CCACHE_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/ccache/ccache/releases/download/v${CCACHE_VERSION}/ccache-${CCACHE_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/ccache-${CCACHE_VERSION}.tar.gz"
fi

tar xf "$DOWNLOADS_DIR/ccache-${CCACHE_VERSION}.tar.gz"

cd "ccache-${CCACHE_VERSION}"
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/aswfbuilder -DZSTD_FROM_INTERNET=ON ..
make -j$(nproc)
make install

ln -s /opt/aswfbuilder/bin/ccache /opt/aswfbuilder/bin/gcc
ln -s /opt/aswfbuilder/bin/ccache /opt/aswfbuilder/bin/g++
ln -s /opt/aswfbuilder/bin/ccache /opt/aswfbuilder/bin/cc
ln -s /opt/aswfbuilder/bin/ccache /opt/aswfbuilder/bin/c++

cd ../../..
rm -rf ccache
