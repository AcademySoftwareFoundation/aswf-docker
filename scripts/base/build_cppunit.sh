#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/cppunit-${ASWF_CPPUNIT_VERSION}.tar.gz" ]; then
    curl --location "http://dev-www.libreoffice.org/src/cppunit-${ASWF_CPPUNIT_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/cppunit-${ASWF_CPPUNIT_VERSION}.tar.gz"
fi

tar xf "$DOWNLOADS_DIR/cppunit-${ASWF_CPPUNIT_VERSION}.tar.gz"
cd "cppunit-${ASWF_CPPUNIT_VERSION}"

./configure --prefix="${ASWF_INSTALL_PREFIX}"
make -j$(nproc)
make install

cd ..
rm -rf "cppunit-${ASWF_CPPUNIT_VERSION}"
