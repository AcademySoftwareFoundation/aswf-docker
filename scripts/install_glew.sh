#!/usr/bin/env bash

set -ex

GLEW_VERSION="$1"

wget https://github.com/nigels-com/glew/releases/download/glew-${GLEW_VERSION}/glew-${GLEW_VERSION}.tgz
tar xf glew-${GLEW_VERSION}.tgz
cd glew-${GLEW_VERSION}/build
cmake ./cmake -DCMAKE_INSTALL_PREFIX=/usr/local
make -j4
make install

cd ../..
rm -rf glew-${GLEW_VERSION}.tgz glew-${GLEW_VERSION}
