#!/usr/bin/env bash

set -ex

git clone https://github.com/Blosc/c-blosc.git
cd c-blosc

if [ "$BLOSC_VERSION" != "latest" ]; then
    git checkout tags/v${BLOSC_VERSION} -b v${BLOSC_VERSION}
fi

mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=${ASWF_INSTALL_PREFIX}
make -j4
make install

cd ../..
rm -rf c-blosc
