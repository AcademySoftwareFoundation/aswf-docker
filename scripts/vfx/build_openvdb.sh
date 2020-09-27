#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/openvdb-${OPENVDB_VERSION}.tar.gz" ]; then
     curl --location "https://github.com/AcademySoftwareFoundation/openvdb/archive/v${OPENVDB_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/openvdb-${OPENVDB_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/openvdb-${OPENVDB_VERSION}.tar.gz"
cd "openvdb-${OPENVDB_VERSION}"

if [[ $OPENVDB_VERSION == 5* ]]; then
cat <<EOF | patch -p1
diff -ur openvdb-5.2.0/openvdb/python/CMakeLists.txt openvdb-5.2.0_patched/openvdb/python/CMakeLists.txt
--- openvdb-5.2.0/openvdb/python/CMakeLists.txt 2018-08-14 01:33:07.000000000 +1000
+++ openvdb-5.2.0_patched/openvdb/python/CMakeLists.txt 2019-11-13 16:19:41.961383996 +1100
@@ -3,7 +3,7 @@
 
 FIND_PACKAGE ( PythonInterp REQUIRED )
 FIND_PACKAGE ( PythonLibs REQUIRED )
-FIND_PACKAGE ( Boost \${MINIMUM_BOOST_VERSION} REQUIRED COMPONENTS python\${PYTHON_VERSION_MAJOR}.\${PYTHON_VERSION_MINOR} )
+FIND_PACKAGE ( Boost \${MINIMUM_BOOST_VERSION} REQUIRED COMPONENTS python )
 
 
 IF ( NOT OPENVDB_BUILD_CORE )
EOF

fi

mkdir build
cd build

cmake \
    -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
    -DOPENEXR_LOCATION="${ASWF_INSTALL_PREFIX}" \
    -DCPPUNIT_LOCATION="${ASWF_INSTALL_PREFIX}" \
    -DBLOSC_LOCATION="${ASWF_INSTALL_PREFIX}" \
    -DTBB_LOCATION="${ASWF_INSTALL_PREFIX}" \
    -DILMBASE_LOCATION="${ASWF_INSTALL_PREFIX}" \
    -DGLFW3_LOCATION="${ASWF_INSTALL_PREFIX}" \
    -DUSE_GLFW3=ON \
    -DGLFW3_USE_STATIC_LIBS=ON \
    -DOPENVDB_BUILD_UNITTESTS=OFF \
    -DOPENVDB_BUILD_VDB_LOD=ON \
    -DOPENVDB_BUILD_VDB_RENDER=ON \
    -DOPENVDB_BUILD_VDB_VIEW=OFF \
    ..

make -j$(nproc)
make install

cd ../..
rm -rf "openvdb-${OPENVDB_VERSION}"
