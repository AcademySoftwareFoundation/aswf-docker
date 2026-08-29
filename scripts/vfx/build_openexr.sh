#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [[ ! -f "$DOWNLOADS_DIR/openexr-${ASWF_OPENEXR_VERSION}.tar.gz" ]]; then
    curl --location "https://github.com/AcademySoftwareFoundation/openexr/archive/v${ASWF_OPENEXR_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/openexr-${ASWF_OPENEXR_VERSION}.tar.gz"
fi

tar xf "$DOWNLOADS_DIR/openexr-${ASWF_OPENEXR_VERSION}.tar.gz"
cd "openexr-${ASWF_OPENEXR_VERSION}"

if [[ $ASWF_OPENEXR_VERSION == 3.2.10 ]]; then

cat << 'EOF' | patch -p1
diff --git a/src/wrappers/python/CMakeLists.txt b/src/wrappers/python/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- a/src/wrappers/python/CMakeLists.txt
+++ b/src/wrappers/python/CMakeLists.txt
@@ -9,9 +9,9 @@
   find_package(OpenEXR)
 endif()

-find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
+find_package(Python3 ${OPENEXR_PYTHON_VERSION} EXACT COMPONENTS Interpreter Development.Module REQUIRED)

-python_add_library (PyOpenEXR MODULE OpenEXR.cpp)
+python3_add_library (PyOpenEXR MODULE OpenEXR.cpp)

 target_link_libraries (PyOpenEXR PRIVATE "${Python_LIBRARIES}" OpenEXR::OpenEXR)

diff --git a/src/test/bin/CMakeLists.txt b/src/test/bin/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- a/src/test/bin/CMakeLists.txt
+++ b/src/test/bin/CMakeLists.txt
@@ -3,7 +3,7 @@

 if(BUILD_TESTING)

-  find_package(Python3 COMPONENTS Interpreter)
+  find_package(Python3 ${OPENEXR_PYTHON_VERSION} EXACT COMPONENTS Interpreter Development.Module REQUIRED)
   if (NOT Python3_FOUND)
     message(STATUS "Python3 not found: skipping bin tests")
     return()
EOF

fi

if [[ $ASWF_OPENEXR_VERSION == 3.3.12 ]]; then

cat << 'EOF' | patch -p1
diff --git a/src/wrappers/python/CMakeLists.txt b/src/wrappers/python/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- a/src/wrappers/python/CMakeLists.txt
+++ b/src/wrappers/python/CMakeLists.txt
@@ -9,10 +9,10 @@
   find_package(OpenEXR)
 endif()

-find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
+find_package(Python3 ${OPENEXR_PYTHON_VERSION} EXACT COMPONENTS Interpreter Development.Module REQUIRED)
 find_package(pybind11 CONFIG REQUIRED)

-python_add_library (PyOpenEXR MODULE PyOpenEXR.cpp PyOpenEXR_old.cpp)
+python3_add_library (PyOpenEXR MODULE PyOpenEXR.cpp PyOpenEXR_old.cpp)

 target_link_libraries (PyOpenEXR PRIVATE "${Python_LIBRARIES}" OpenEXR::OpenEXR pybind11::headers)

diff --git a/src/test/bin/CMakeLists.txt b/src/test/bin/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- a/src/test/bin/CMakeLists.txt
+++ b/src/test/bin/CMakeLists.txt
@@ -3,7 +3,7 @@

 if(BUILD_TESTING)

-  find_package(Python3 COMPONENTS Interpreter)
+  find_package(Python3 ${OPENEXR_PYTHON_VERSION} EXACT COMPONENTS Interpreter Development.Module REQUIRED)
   if (NOT Python3_FOUND)
     message(STATUS "Python3 not found: skipping bin tests")
     return()
EOF

fi

if [[ $ASWF_OPENEXR_VERSION == 3.4.15 ]]; then

cat << 'EOF' | patch -p1
diff --git a/src/wrappers/python/CMakeLists.txt b/src/wrappers/python/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- a/src/wrappers/python/CMakeLists.txt
+++ b/src/wrappers/python/CMakeLists.txt
@@ -9,10 +9,10 @@
   find_package(OpenEXR)
 endif()

-find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)
+find_package(Python3 ${OPENEXR_PYTHON_VERSION} EXACT COMPONENTS Interpreter Development.Module REQUIRED)
 find_package(pybind11 CONFIG REQUIRED)

-Python3_add_library (PyOpenEXR MODULE WITH_SOABI PyOpenEXR.cpp PyOpenEXR_old.cpp)
+python3_add_library (PyOpenEXR MODULE WITH_SOABI PyOpenEXR.cpp PyOpenEXR_old.cpp)
 target_link_libraries (PyOpenEXR PRIVATE "${Python3_LIBRARIES}" OpenEXR::OpenEXR pybind11::headers)

 # The python module should be called "OpenEXR.x", not "PyOpenEXR.x".
diff --git a/src/test/bin/CMakeLists.txt b/src/test/bin/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- a/src/test/bin/CMakeLists.txt
+++ b/src/test/bin/CMakeLists.txt
@@ -3,7 +3,7 @@

 if(BUILD_TESTING)

-  find_package(Python3 COMPONENTS Interpreter)
+  find_package(Python3 ${OPENEXR_PYTHON_VERSION} EXACT COMPONENTS Interpreter Development.Module REQUIRED)
   if (NOT Python3_FOUND)
     message(STATUS "Python3 not found: skipping bin tests")
     return()
EOF

fi

mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
    -DOPENEXR_BUILD_PYTHON="on" \
    -DOPENEXR_PYTHON_VERSION="${ASWF_CONAN_PYTHON_VERSION}" \
    ..
cmake --build . -j$(nproc)
cmake --install .

cd ../..
rm -rf "openexr-${ASWF_OPENEXR_VERSION}"
