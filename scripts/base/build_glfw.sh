#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

git clone https://github.com/glfw/glfw.git
cd glfw

if [ "$ASWF_GLFW_VERSION" != "latest" ]; then
    git checkout "tags/${ASWF_GLFW_VERSION}" -b "${ASWF_GLFW_VERSION}"
fi

mkdir build
cd build

cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" ..
make -j$(nproc)
make install

cd ../..
rm -rf glfw
