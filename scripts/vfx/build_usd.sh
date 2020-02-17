#!/usr/bin/env bash
set -ex

pip install jinja2 PyOpenGL

if [ ! -f $DOWNLOADS_DIR/usd-${USD_VERSION}.tar.gz ]; then
     curl --location https://github.com/PixarAnimationStudios/USD/archive/v${USD_VERSION}.tar.gz -o $DOWNLOADS_DIR/usd-${USD_VERSION}.tar.gz
fi

tar -zxf $DOWNLOADS_DIR/usd-${USD_VERSION}.tar.gz
cd USD-${USD_VERSION}

touch pxr/base/lib/vt/devtoolset6Workaround.cpp
echo '#if (__GNUC__ >= 6)
#include <cstdlib>
#pragma weak __cxa_throw_bad_array_new_length
extern "C" void __cxa_throw_bad_array_new_length()
{
 abort();
}
#endif' >> pxr/base/lib/vt/devtoolset6Workaround.cpp

patch -p1 <<EOF
diff --git a/pxr/base/lib/vt/CMakeLists.txt b/pxr/base/lib/vt/CMakeLists.txt
index aecffd7fb..c8f840bed 100644
--- a/pxr/base/lib/vt/CMakeLists.txt
+++ b/pxr/base/lib/vt/CMakeLists.txt
@@ -38,6 +38,9 @@ pxr_library(vt
 
     PRIVATE_HEADERS
         typeHeaders.h
+        
+    CPPFILES
+        devtoolset6Workaround.cpp
 
     PYTHON_CPPFILES
         moduleDeps.cpp
EOF

mkdir build
cd build

cmake \
     -DCMAKE_INSTALL_PREFIX=${ASWF_INSTALL_PREFIX} \
     -DOPENEXR_LOCATION=${ASWF_INSTALL_PREFIX} \
     -DCPPUNIT_LOCATION=${ASWF_INSTALL_PREFIX} \
     -DBLOSC_LOCATION=${ASWF_INSTALL_PREFIX} \
     -DTBB_LOCATION=${ASWF_INSTALL_PREFIX} \
     -DILMBASE_LOCATION=${ASWF_INSTALL_PREFIX} \
     -DPXR_BUILD_TESTS=OFF \
     -DUSD_ROOT_DIR=$ASWF_INSTALL_PREFIX \
     -DPXR_BUILD_ALEMBIC_PLUGIN=OFF \
     -DPXR_BUILD_MAYA_PLUGIN=FALSE \
     ..

make -j$(nproc)
make install

cd ../..

rm -rf USD-${USD_VERSION}
