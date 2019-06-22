#!/usr/bin/env bash

set -ex

CLANG_VERSION="$1"

wget https://github.com/llvm/llvm-project/archive/llvmorg-${CLANG_VERSION}.tar.gz
tar xf llvmorg-${CLANG_VERSION}.tar.gz
cd llvm-project-llvmorg-${CLANG_VERSION}

mkdir build
cd build
cmake -DLLVM_ENABLE_PROJECTS=clang \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLVM_TARGETS_TO_BUILD=host \
      -DCMAKE_INSTALL_PREFIX=/usr/local \
      ../llvm
make -j2
make install

cd ../..
rm -rf llvm-project-llvmorg-${CLANG_VERSION}
