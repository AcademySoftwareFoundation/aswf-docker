#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [[ ! -f "$DOWNLOADS_DIR/-${ASWF_OPENVDB_VERSION}.tar.gz" ]]; then
     curl --location "https://github.com/AcademySoftwareFoundation/OpenImageIO/archive/v${ASWF_OIIO_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/oiio-${ASWF_OIIO_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/oiio-${ASWF_OIIO_VERSION}.tar.gz"
cd "OpenImageIO-${ASWF_OIIO_VERSION}"

if [[ $ASWF_OIIO_VERSION == 3.1.10.0 ]]; then

cat << 'EOF' | patch -p1
diff --git a/src/cmake/dependency_utils.cmake b/src/cmake/dependency_utils.cmake
index d99dd79ac..bfda2778a 100644
--- a/src/cmake/dependency_utils.cmake
+++ b/src/cmake/dependency_utils.cmake
@@ -402,6 +402,11 @@
             # was already found, or we're forcing a local build
         elseif (_pkg_CONFIG OR _pkg_PREFER_CONFIG OR ${PROJECT_NAME}_ALWAYS_PREFER_CONFIG)
             find_package (${pkgname} ${_${pkgname}_version_range} CONFIG ${_pkg_UNPARSED_ARGUMENTS})
+            if (${pkgname} STREQUAL "OpenJPEG" AND NOT DEFINED OPENJPEG_VERSION )
+                # EL8 CMake doesnt set OpenJPEG_VERSION
+                set (OPENJPEG_VERSION "${OPENJPEG_MAJOR_VERSION}.${OPENJPEG_MINOR_VERSION}.${OPENJPEG_BUILD_VERSION}")
+                set (OpenJPEG_VERSION "${OPENJPEG_MAJOR_VERSION}.${OPENJPEG_MINOR_VERSION}.${OPENJPEG_BUILD_VERSION}")
+            endif ()
             reject_out_of_range_versions (${pkgname} "${${pkgname}_VERSION}"
                                           ${_pkg_VERSION_MIN} ${_pkg_VERSION_MAX}
                                           _pkg_version_in_range)
diff --git a/src/jpeg2000.imageio/CMakeLists.txt b/src/jpeg2000.imageio/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- a/src/jpeg2000.imageio/CMakeLists.txt
--- b/src/jpeg2000.imageio/CMakeLists.txt
@@ -10,6 +10,7 @@
         set (OPENJPEG_TARGET openjp2_static)
     elseif (TARGET openjp2)
         set (OPENJPEG_TARGET openjp2)
+        set(_jpeg2000_includes ${OPENJPEG_INCLUDE_DIRS})
     else ()
         set(_jpeg2000_includes ${OPENJPEG_INCLUDES})
         set(_jpeg2000_lib_dirs ${OPENJPEG_LIBRARY_DIRS})
EOF

fi

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
      -DOIIO_BUILD_TOOLS=ON \
      -DOIIO_BUILD_TESTS=OFF \
      -DUSE_QT=ON \
      -DVERBOSE=ON \
      -DPYTHON_VERSION="${ASWF_PYTHON_MAJOR_MINOR_VERSION}" \
      -DBoost_NO_BOOST_CMAKE=ON \
      -Dpybind11_ROOT="${ASWF_INSTALL_PREFIX}" \
      -DCMAKE_CXX_STANDARD="${ASWF_CXX_STANDARD}" \
      ../.
cmake --build . -j$(nproc)
cmake --install .

cd ../..
rm -rf oiio
