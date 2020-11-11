#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir opensubdiv
cd opensubdiv

if [ ! -f "$DOWNLOADS_DIR/opensubdiv-${ASWF_OPENSUBDIV_VERSION}.tar.gz" ]; then
     curl --location "https://github.com/PixarAnimationStudios/OpenSubdiv/archive/v${ASWF_OPENSUBDIV_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/opensubdiv-${ASWF_OPENSUBDIV_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/opensubdiv-${ASWF_OPENSUBDIV_VERSION}.tar.gz"
cd "OpenSubdiv-${ASWF_OPENSUBDIV_VERSION}"

# Apply cmake patch https://github.com/PixarAnimationStudios/OpenSubdiv/pull/952
cat <<EOF | patch -p1
diff --git a/CMakeLists.txt b/CMakeLists.txt
index 4f3cd9d40..e01dc0915 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -48,7 +48,7 @@ endif()
     string(REGEX REPLACE "^v" "" OSD_SONAME \${OSD_SONAME})
 
     add_definitions(
-        -DOPENSUBDIV_VERSION_STRING="\${OSD_SONAME}"
+        -DOPENSUBDIV_VERSION_STRING=\\\"\${OSD_SONAME}\\\"
     )
 
 #-------------------------------------------------------------------------------
EOF

if [[ $ASWF_DTS_VERSION == 9 && $ASWF_CUDA_VERSION == 10* ]]; then
    CUDA_COMPUTE_VERSION=compute_30
else
    CUDA_COMPUTE_VERSION=compute_50
fi

mkdir build
cd build

cmake .. \
      -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
      -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda \
      -DOPENCL_INCLUDE_DIRS=/usr/local/cuda/include \
      -DOPENCL_LIBRARIES=/usr/local/cuda/lib64/libOpenCL.so \
      -DTBB_LOCATION="${ASWF_INSTALL_PREFIX}" \
      -DPTEX_INCLUDE_DIR="${ASWF_INSTALL_PREFIX}/include" \
      -DPTEX_LOCATION="${ASWF_INSTALL_PREFIX}" \
      -DGLFW_LOCATION="${ASWF_INSTALL_PREFIX}" \
      -DGLEW_INCLUDE_DIR="${ASWF_INSTALL_PREFIX}/include" \
      -DNO_EXAMPLES=ON \
      -DNO_REGRESSION=1 \
      -DNO_DOC=1 \
      -DNO_TUTORIALS=ON \
      -DOSD_CUDA_NVCC_FLAGS="--gpu-architecture ${CUDA_COMPUTE_VERSION}"
make # random cuda build failure when more than one job in //...
make install

cd ../../..
rm -rf opensubdiv
