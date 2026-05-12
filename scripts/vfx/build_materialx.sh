#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir materialx
cd materialx

if [[ ! -f "$DOWNLOADS_DIR/materialx-${ASWF_MATERIALX_VERSION}.tar.gz" ]]; then
    curl --location "https://github.com/AcademySoftwareFoundation/MaterialX/archive/v${ASWF_MATERIALX_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/materialx-${ASWF_MATERIALX_VERSION}.tar.gz"
fi
tar -zxf "$DOWNLOADS_DIR/materialx-${ASWF_MATERIALX_VERSION}.tar.gz"
cd "MaterialX-${ASWF_MATERIALX_VERSION}"

if [[ $ASWF_MATERIALX_VERSION == 1.38.7 ]]; then

cat << 'EOF' | patch -p1
diff --git a/CMakeLists.txt b/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -6,7 +6,7 @@

 # Cmake setup
 cmake_minimum_required(VERSION 3.1)
-set(CMAKE_CXX_STANDARD 11)
+set(CMAKE_CXX_STANDARD 17)
 set(CMAKE_POSITION_INDEPENDENT_CODE TRUE)
 set(CMAKE_MACOSX_RPATH ON)
 enable_testing()
EOF

fi

mkdir build
cd build
# Can't enable MATERIALX_BUILD_VIEWER until we provide NanoGUI
# Can't enable MATERIALX_BUILD_GRAPH_EDITOR until we provide ImGUI
cmake \
    -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
    -DMATERIALX_BUILD_PYTHON=ON \
    -DMATERIALX_BUILD_VIEWER=OFF \
    -DMATERIALX_BUILD_GRAPH_EDITOR=OFF \
    -DMATERIALX_BUILD_SHARED_LIBS=ON \
    -DMATERIALX_BUILD_OIIO=ON \
    -DMATERIALX_BUILD_OCIO=ON \
    -DMATERIALX_INSTALL_STDLIB_PATH="share/MaterialX/libraries" \
    -DMATERIALX_INSTALL_RESOURCES_PATH="share/MaterialX/resources" \
    -DMATERIALX_PYTHON_FOLDER_NAME="share/MateriaX/python" \
    ..
cmake --build . -j$(nproc)
cmake --install .

cd ../..
rm -rf materialx
