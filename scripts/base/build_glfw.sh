#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

git clone https://github.com/glfw/glfw.git
cd glfw

if [ "$GLFW_VERSION" != "latest" ]; then
    git checkout tags/${GLFW_VERSION} -b ${GLFW_VERSION}
fi

mkdir build
cd build

cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=${ASWF_INSTALL_PREFIX} ..
make -j4
make install

cd ../..
rm -rf glfw
