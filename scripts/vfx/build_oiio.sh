#!/usr/bin/env bash

set -ex

git clone https://github.com/OpenImageIO/oiio.git
cd oiio

if [ "$OIIO_VERSION" != "latest" ]; then
    git checkout tags/Release-${OIIO_VERSION} -b Release-${OIIO_VERSION}
fi

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=${ASWF_INSTALL_PREFIX} \
      -DOIIO_BUILD_TOOLS=OFF \
      -DOIIO_BUILD_TESTS=OFF \
      -DVERBOSE=ON \
      -DPYTHON_VERSION=${PYTHON_VERSION} \
      -DBoost_NO_BOOST_CMAKE=ON \
      ../.
make -j4
make install

cd ../..
rm -rf oiio
