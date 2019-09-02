#!/usr/bin/env bash

set -ex

curl --location https://github.com/openexr/openexr/archive/v${OPENEXR_VERSION}.tar.gz -o openexr.tar.gz
tar xf openexr.tar.gz && rm openexr.tar.gz
cd openexr-${OPENEXR_VERSION}

if [[ $OPENEXR_VERSION == 2.2* ]]; then

    cd IlmBase
    ./bootstrap
    ./configure --prefix=/usr/local
    make -j4
    make install

    cd ../OpenEXR
    ./bootstrap
    ./configure --prefix=/usr/local
    make -j4
    make install

    cd ../PyIlmBase
    ./bootstrap
    ./configure --prefix=/usr/local
    make -j4
    make install
else

    # TODO: add support for python-3 PyIlmBase when it works...
    if [[ $OPENEXR_VERSION == 2.3.0 ]]; then
        if [[ $PYTHON_VERSION == 2.7* ]]; then
            BUILD_PYILMBASE=on
        else
            BUILD_PYILMBASE=off
        fi
    else
        BUILD_PYILMBASE=on
    fi

    mkdir build
    cd build
    cmake \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DOPENEXR_BUILD_PYTHON_LIBS=${BUILD_PYILMBASE} \
        ..
    make -j4
    make install
fi

cd ../..
rm -rf openexr-${OPENEXR_VERSION}
