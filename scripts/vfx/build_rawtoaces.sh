#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir rawtoaces
cd rawtoaces

ASWF_RAWTOACES_VERSION_DOWNLOAD=${ASWF_RAWTOACES_VERSION}
if [[ ${ASWF_RAWTOACES_VERSION_DOWNLOAD} == 1.1.0 ]]; then
    # asset name doesn't match version
    ASWF_RAWTOACES_VERSION_DOWNLOAD=1.1
fi

if [[ ! -f "$DOWNLOADS_DIR/rawtoaces-${ASWF_RAWTOACES_VERSION_DOWNLOAD}.tar.gz" ]]; then
    curl --location "https://github.com/AcademySoftwareFoundation/rawtoaces/archive/refs/tags/v${ASWF_RAWTOACES_VERSION_DOWNLOAD}.tar.gz" -o "$DOWNLOADS_DIR/rawtoaces-${ASWF_RAWTOACES_VERSION_DOWNLOAD}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/rawtoaces-${ASWF_RAWTOACES_VERSION_DOWNLOAD}.tar.gz"
cd "rawtoaces-${ASWF_RAWTOACES_VERSION_DOWNLOAD}"

if [[ $ASWF_RAWTOACES_VERSION == 2.1.1 ]]; then

# Don't use single quotes around EOF to allow ASWF_CONAN_PYTHON_VERSION to be expanded
cat << 'EOF' | patch -p1
diff --git a/configure.cmake b/configure.cmake
index d99dd79ac..bfda2778a 100644
--- a/configure.cmake
+++ b/configure.cmake
@@ -25,7 +25,7 @@
         set( DEV_MODULE Development.Module )
     endif ()
 
-    find_package ( Python 3.8 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED )
+    find_package ( Python ${RTA_PYTHON_VERSION} EXACT COMPONENTS Interpreter ${DEV_MODULE} REQUIRED )
 
     execute_process (
         COMMAND "\${Python_EXECUTABLE}" -m nanobind --cmake_dir
EOF

fi

mkdir build
cd build
cmake \
     -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
     -DRTA_BUILD_PYTHON_BINDINGS="ON" \
     -DRTA_PYTHON_VERSION="${ASWF_CONAN_PYTHON_VERSION}" \
     -DRTA_ENABLE_LENSFUN="ON" \
     -DRTA_ENABLE_EIGEN="ON" \
     ..
cmake --build . -j$(nproc)
cmake --install .

cd ../../..
rm -rf rawtoaces
