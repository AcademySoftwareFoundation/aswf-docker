#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir ocio
cd ocio

if [[ ! -f "$DOWNLOADS_DIR/ocio-${ASWF_OPENCOLORIO_VERSION}.tar.gz" ]]; then
    curl --location "https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/v${ASWF_OPENCOLORIO_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/ocio-${ASWF_OPENCOLORIO_VERSION}.tar.gz"
fi
tar -zxf "$DOWNLOADS_DIR/ocio-${ASWF_OPENCOLORIO_VERSION}.tar.gz"
cd "OpenColorIO-${ASWF_OPENCOLORIO_VERSION}"

if [[ $ASWF_OPENCOLORIO_VERSION == 2.2.1 ]]; then

cat << 'EOF' | patch -p1
diff --git a/share/cmake/modules/Findyaml-cpp.cmake b/share/cmake/modules/Findyaml-cpp.cmake
index d99dd79ac..bfda2778a 100644
--- a/share/cmake/modules/Findyaml-cpp.cmake
+++ b/share/cmake/modules/Findyaml-cpp.cmake
@@ -43,7 +43,8 @@
     endif()

     if(yaml-cpp_FOUND)
-        get_target_property(yaml-cpp_LIBRARY yaml-cpp LOCATION)
+        get_target_property(yaml-cpp_INCLUDE_DIR yaml-cpp::yaml-cpp INTERFACE_INCLUDE_DIRECTORIES)
+        get_target_property(yaml-cpp_LIBRARY yaml-cpp::yaml-cpp IMPORTED_LOCATION_RELEASE)
     else()

         # As yaml-cpp-config.cmake search fails, search an installed library
EOF

fi

mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
    -DOCIO_USE_OIIO_FOR_APPS=OFF \
    -DOCIO_BUILD_STATIC=OFF \
    -DOCIO_BUILD_APPS=ON \
    -DOCIO_BUILD_NUKE=OFF \
    -DOCIO_INSTALL_EXT_PACKAGES=MISSING \
    -Dpybind11_ROOT="${ASWF_INSTALL_PREFIX}" \
    -DGLEW_ROOT="${ASWF_INSTALL_PREFIX}" \
    -DCMAKE_CXX_FLAGS="-Wno-error=unused-function -Wno-error=deprecated-declarations"\
    ..
cmake --build . -j$(nproc)
cmake --install .

# As per the OCIO Slack #dev channel, we no longer need to download  OCIO configs
# separately, the 2.x configs are now built-in to the library.
# Legacy 1.x configs: https://github.com/colour-science/OpenColorIO-Configs
# 2.x config source: https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES

cd ../..
rm -rf ocio
