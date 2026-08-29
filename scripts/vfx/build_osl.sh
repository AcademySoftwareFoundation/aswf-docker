#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [[ ! -f "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz" ]]; then
    curl --location "https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/archive/refs/tags/v${ASWF_OSL_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz"
cd "OpenShadingLanguage-${ASWF_OSL_VERSION}"

if [[ $ASWF_OSL_VERSION == 1.13.11.0 ]]; then
# Serialize CUDA builds to avoid race condition

cat << 'EOF' | patch -p1
diff --git a/src/testshade/CMakeLists.txt b/src/testshade/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- a/src/testshade/CMakeLists.txt
+++ b/src/testshade/CMakeLists.txt
@@ -80,6 +80,9 @@
 target_link_libraries (testshade
                        PRIVATE
                            oslexec oslquery)
+if (OSL_USE_OPTIX)
+    add_dependencies(testshade testshade_ptx)
+endif ()

 install (TARGETS testshade RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} )

@@ -96,6 +99,7 @@
 if (NOT CODECOV)
     # The 'libtestshade' library
     add_library ( "libtestshade" ${testshade_srcs} )
+    add_dependencies(libtestshade testshade)

     set_target_properties (libtestshade
                            PROPERTIES
EOF

fi

if [[ $ASWF_OSL_VERSION == 1.15.6.0 ]]; then
# Parallel CUDA build race condition fix

cat << 'EOF' | patch -p1
diff --git a/src/testrender/CMakeLists.txt b/src/testrender/CMakeLists.txt
index d99dd79ac..bfda2778a 100644
--- a/src/testrender/CMakeLists.txt
+++ b/src/testrender/CMakeLists.txt
@@ -85,6 +85,10 @@
         pugixml::pugixml
         Threads::Threads)

+if (OSL_USE_OPTIX)
+    add_dependencies(testrender testrender_ptx)
+endif ()
+
 osl_optix_target (testrender)

 install ( TARGETS testrender RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} )
EOF

fi

if [[ ${ASWF_CUDA_VERSION%%.*} -ge 13 ]]; then
    CUDA_TARGET_ARCH=sm_75
else
    CUDA_TARGET_ARCH=sm_50
fi

mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
      -DBoost_USE_STATIC_LIBS=OFF \
      -DBUILD_SHARED_LIBS=ON \
      -DCMAKE_CXX_STANDARD=$ASWF_CXX_STANDARD \
      -Dpybind11_DIR="${ASWF_INSTALL_PREFIX}/lib/cmake/pybind11" \
      -DOSL_USE_OPTIX=ON \
      -DOPTIX_VERSION=${ASWF_OPTIX_VERSION} \
      -DOPTIXHOME=${ASWF_INSTALL_PREFIX}/NVIDIA-OptiX-SDK-${ASWF_OPTIX_VERSION} \
      -DCUDA_TARGET_ARCH=${CUDA_TARGET_ARCH} \
      -DPYTHON_VERSION=${ASWF_CONAN_PYTHON_VERSION} \
      ../.
cmake --build . -j$(nproc)
cmake --install .

cd ../..
rm -rf "OpenShadingLanguage-${ASWF_OSL_VERSION}"
