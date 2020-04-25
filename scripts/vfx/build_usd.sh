#!/usr/bin/env bash
set -ex

pip install jinja2 PyOpenGL

if [ ! -f $DOWNLOADS_DIR/usd-${USD_VERSION}.tar.gz ]; then
     curl --location https://github.com/PixarAnimationStudios/USD/archive/v${USD_VERSION}.tar.gz -o $DOWNLOADS_DIR/usd-${USD_VERSION}.tar.gz
fi

tar -zxf $DOWNLOADS_DIR/usd-${USD_VERSION}.tar.gz
cd USD-${USD_VERSION}

if [[ $USD_VERSION == 19.* ]]; then
     VT_SRC_FOLDER=base/lib/vt
else
     VT_SRC_FOLDER=base/vt
fi

touch pxr/${VT_SRC_FOLDER}/devtoolset6Workaround.cpp
echo '#if (__GNUC__ >= 6)
#include <cstdlib>
#pragma weak __cxa_throw_bad_array_new_length
extern "C" void __cxa_throw_bad_array_new_length()
{
 abort();
}
#endif' >> pxr/${VT_SRC_FOLDER}/devtoolset6Workaround.cpp

patch -p1 <<EOF
diff --git a/pxr/${VT_SRC_FOLDER}/CMakeLists.txt b/pxr/${VT_SRC_FOLDER}/CMakeLists.txt
index aecffd7fb..c8f840bed 100644
--- a/pxr/${VT_SRC_FOLDER}/CMakeLists.txt
+++ b/pxr/${VT_SRC_FOLDER}/CMakeLists.txt
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

if [[ $PYTHON_VERSION == 2.7* ]]; then
    USD_EXTRA_ARGS=
else
    USD_EXTRA_ARGS=-DPXR_USE_PYTHON_3=ON
fi

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
     ${USD_EXTRA_ARGS} \
     ..

make -j$(nproc)
make install

cd ../..

rm -rf USD-${USD_VERSION}
