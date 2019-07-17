#!/usr/bin/env bash

set -ex

curl --location https://github.com/nigels-com/glew/releases/download/glew-${GLEW_VERSION}/glew-${GLEW_VERSION}.tgz -o glew.tgz
tar xf glew.tgz && rm glew.tgz

cd glew-${GLEW_VERSION}/build
cmake ./cmake -DCMAKE_INSTALL_PREFIX=/usr/local
make -j4
make install

cd ../..
rm -rf glew-${GLEW_VERSION}.tgz glew-${GLEW_VERSION}
