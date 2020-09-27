#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir ccache
cd ccache

CCACHE_VERSION=3.7.9
if [ ! -f "$DOWNLOADS_DIR/ccache-${CCACHE_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/ccache/ccache/releases/download/v${CCACHE_VERSION}/ccache-${CCACHE_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/ccache-${CCACHE_VERSION}.tar.gz"
fi

tar xf "$DOWNLOADS_DIR/ccache-${CCACHE_VERSION}.tar.gz"

cd "ccache-${CCACHE_VERSION}"
./configure --prefix=/opt/aswfbuilder
make -j$(nproc)
make install

ln -s /opt/aswfbuilder/bin/ccache /opt/aswfbuilder/bin/gcc
ln -s /opt/aswfbuilder/bin/ccache /opt/aswfbuilder/bin/g++
ln -s /opt/aswfbuilder/bin/ccache /opt/aswfbuilder/bin/cc
ln -s /opt/aswfbuilder/bin/ccache /opt/aswfbuilder/bin/c++

cd ../..
rm -rf ccache
