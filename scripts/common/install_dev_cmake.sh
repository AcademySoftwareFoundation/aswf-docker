#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir -p /opt/aswfbuilder

export DEV_CMAKE_VERSION=3.12.4

if [ ! -f "$DOWNLOADS_DIR/cmake-${DEV_CMAKE_VERSION}-Linux-x86_64.sh" ]; then
    curl --location "https://github.com/Kitware/CMake/releases/download/v${DEV_CMAKE_VERSION}/cmake-${DEV_CMAKE_VERSION}-Linux-x86_64.sh" -o "$DOWNLOADS_DIR/cmake-${DEV_CMAKE_VERSION}-Linux-x86_64.sh"
fi
sh "$DOWNLOADS_DIR/cmake-${DEV_CMAKE_VERSION}-Linux-x86_64.sh" --skip-license --prefix=/opt/aswfbuilder --exclude-subdir
