#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir openfx
cd openfx

if [ ! -f "$DOWNLOADS_DIR/ptex-${ASWF_OPENFX_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/AcademySoftwareFoundation/openfx/archive/refs/tags/OFX_Release_${ASWF_OPENFX_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/openfx-${ASWF_OPENFX_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/openfx-${ASWF_OPENFX_VERSION}.tar.gz"
cd "openfx-OFX_Release_${ASWF_OPENFX_VERSION}"

# Fix up CMakeLists.txt

cat << 'EOF' | patch -p1
diff --git a/CMakeLists.txt b/CMakeLists.txt
index 6cf74b219a1..501394deede 10064
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -38,8 +38,7 @@
   add_definitions(-DOFX_SUPPORTS_OPENGLRENDER)
 endif()
 if(OFX_SUPPORTS_OPENCLRENDER)
-  find_package(OpenCLHeaders REQUIRED)
-  find_package(OpenCLICDLoader REQUIRED)
+  find_package(OpenCL REQUIRED)
   add_definitions(-DOFX_SUPPORTS_OPENCLRENDER)
 endif()
 if(OFX_SUPPORTS_CUDARENDER)
@@ -62,9 +61,10 @@

 # Conan packages
 find_package(EXPAT)
-find_package(opengl_system REQUIRED)
-find_package(cimg REQUIRED)
+find_package(OpenGL REQUIRED)
+#find_package(cimg REQUIRED)
 find_package(spdlog REQUIRED)
+find_package(expat REQUIRED)

 # Macros
 include(OpenFX)
diff --git a/Examples/CMakeLists.txt b/Examples/CMakeLists.txt
index 6cf74b219a1..501394deede 10064
--- a/Examples/CMakeLists.txt
+++ b/Examples/CMakeLists.txt
@@ -22,11 +22,11 @@
 	target_link_libraries(${TGT} ${CONAN_LIBS})
 	target_include_directories(${TGT} PUBLIC ${OFX_HEADER_DIR} ${OFX_SUPPORT_HEADER_DIR})
         if (OFX_SUPPORTS_OPENCLRENDER)
-          target_link_libraries(${TGT} PRIVATE OpenCL::Headers OpenCL::OpenCL)
+          target_link_libraries(${TGT} PRIVATE OpenCL::OpenCL)
         endif()
 endforeach()

-target_link_libraries(example-OpenGL PRIVATE opengl::opengl)
-target_link_libraries(example-Custom PRIVATE opengl::opengl)
-target_link_libraries(example-ColourSpace PRIVATE cimg::cimg)
+target_link_libraries(example-OpenGL PRIVATE OpenGL::GL)
+target_link_libraries(example-Custom PRIVATE OpenGL::GL)
+#target_link_libraries(example-ColourSpace PRIVATE cimg::cimg)
 target_link_libraries(example-ColourSpace PRIVATE spdlog::spdlog_header_only)
diff --git a/Support/Plugins/CMakeLists.txt b/Support/Plugins/CMakeLists.txt
index 6cf74b219a1..501394deede 10064
--- a/Support/Plugins/CMakeLists.txt
+++ b/Support/Plugins/CMakeLists.txt
@@ -31,7 +31,7 @@
 	set(TGT example-${PLUGIN}-support)
 	add_ofx_plugin(${TGT} ${PLUGIN})
 	target_sources(${TGT} PUBLIC ${PLUGIN_SOURCES})
-	target_link_libraries(${TGT} ${CONAN_LIBS} OfxSupport opengl::opengl)
+	target_link_libraries(${TGT} ${CONAN_LIBS} OfxSupport OpenGL::GL)
 	target_include_directories(${TGT} PUBLIC ${OFX_HEADER_DIR} ${OFX_SUPPORT_HEADER_DIR})
         if(APPLE)
           target_link_libraries(${TGT} "-framework Metal" "-framework Foundation" "-framework QuartzCore")
@@ -40,7 +40,7 @@
           endif()
         else()
           if (OFX_SUPPORTS_OPENCLRENDER)
-            target_link_libraries(${TGT} OpenCL::Headers OpenCL::OpenCL)
+            target_link_libraries(${TGT} OpenCL::OpenCL)
           endif()
         endif()

diff --git a/Support/PropTester/CMakeLists.txt b/Support/PropTester/CMakeLists.txt
index 6cf74b219a1..501394deede 10064
--- a/Support/PropTester/CMakeLists.txt
+++ b/Support/PropTester/CMakeLists.txt
@@ -3,5 +3,5 @@
 set(TGT example-PropTester)
 add_ofx_plugin(${TGT} ${CMAKE_CURRENT_SOURCE_DIR})
 target_sources(${TGT} PUBLIC ${PLUGIN_SOURCES})
-target_link_libraries(${TGT} ${CONAN_LIBS} OfxSupport opengl::opengl)
+target_link_libraries(${TGT} ${CONAN_LIBS} OfxSupport OpenGL::GL)
 target_include_directories(${TGT} PUBLIC ${OFX_HEADER_DIR} ${OFX_SUPPORT_HEADER_DIR})
EOF

mkdir build
cd build
cmake \
     -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
     -DOFX_SUPPORTS_OPENGLRENDER=ON \
     -DOFX_SUPPORTS_OPENCLRENDER=ON \
     -DOFX_SUPPORTS_CUDARENDER=ON \
     -DBUILD_EXAMPLE_PLUGINS=ON \
     -DCMAKE_CUDA_ARCHITECTURES=all-major \
     -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc \
     ..
cmake --build . -j$(nproc)
cmake --install .

cd ../../..
rm -rf openfx
