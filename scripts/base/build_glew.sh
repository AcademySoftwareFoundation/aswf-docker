#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/glew-${ASWF_GLEW_VERSION}.tgz" ]; then
    curl --location "https://github.com/nigels-com/glew/releases/download/glew-${ASWF_GLEW_VERSION}/glew-${ASWF_GLEW_VERSION}.tgz" -o "$DOWNLOADS_DIR/glew-${ASWF_GLEW_VERSION}.tgz"
fi

tar xf "$DOWNLOADS_DIR/glew-${ASWF_GLEW_VERSION}.tgz"

cd "glew-${ASWF_GLEW_VERSION}/build"
cmake ./cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}"
make -j$(nproc)
make install

cd ../..
rm -rf "glew-${ASWF_GLEW_VERSION}"
