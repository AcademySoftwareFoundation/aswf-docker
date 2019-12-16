#!/usr/bin/env bash

set -ex

if [ ! -f $DOWNLOADS_DIR/glew-${GLEW_VERSION}.tgz ]; then
    curl --location https://github.com/nigels-com/glew/releases/download/glew-${GLEW_VERSION}/glew-${GLEW_VERSION}.tgz -o $DOWNLOADS_DIR/glew-${GLEW_VERSION}.tgz
fi

tar xf $DOWNLOADS_DIR/glew-${GLEW_VERSION}.tgz

cd glew-${GLEW_VERSION}/build
cmake ./cmake -DCMAKE_INSTALL_PREFIX=${ASWF_INSTALL_PREFIX}
make -j4
make install

cd ../..
rm -rf glew-${GLEW_VERSION}
