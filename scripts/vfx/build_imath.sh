#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [[ ! -f "$DOWNLOADS_DIR/Imath-${ASWF_IMATH_VERSION}.tar.gz" ]]; then
    curl --location "https://github.com/AcademySoftwareFoundation/Imath/archive/v${ASWF_IMATH_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/Imath-${ASWF_IMATH_VERSION}.tar.gz"
fi

tar xf "$DOWNLOADS_DIR/Imath-${ASWF_IMATH_VERSION}.tar.gz"
cd "Imath-${ASWF_IMATH_VERSION}"

if [[ $ASWF_IMATH_VERSION == 3.1.12 ]]; then
cat << 'EOF' | patch -p0
diff --git src/python/CMakeLists.txt src/python/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- src/python/CMakeLists.txt
+++ src/python/CMakeLists.txt
@@ -46,7 +46,7 @@
   set(Python_EXECUTABLE ${Python2_EXECUTABLE})
   set(Python_SITEARCH ${Python2_SITEARCH})
 else()
-  find_package(Python3 COMPONENTS Interpreter Development)
+  find_package(Python3 ${IMATH_PYTHON_VERSION} EXACT REQUIRED COMPONENTS Interpreter Development)
   if(Python3_FOUND)
     message(STATUS "Found Python ${Python3_VERSION}")
   elseif(Python3::Python)
EOF
fi

if [[ $ASWF_IMATH_VERSION == 3.2.3 ]]; then
cat << 'EOF' | patch -p0
diff --git src/python/CMakeLists.txt src/python/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- src/python/CMakeLists.txt
+++ src/python/CMakeLists.txt
@@ -7,7 +7,7 @@
 # Python and Boost
 #

-find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
+find_package(Python3 ${IMATH_PYTHON_VERSION} EXACT REQUIRED COMPONENTS Interpreter Development)

 if(NOT Python3_FOUND)
     message(FATAL_ERROR "Could not find Python")
EOF
fi

mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
    -DPYTHON=ON \
    -DIMATH_PYTHON_VERSION="${ASWF_CONAN_PYTHON_VERSION}" \
    ..
cmake --build . -j$(nproc) --verbose
cmake --install .

cd ../..
rm -rf $IMATH_FOLDER
