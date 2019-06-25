#!/usr/bin/env bash

set -ex

curl --location https://github.com/llvm/llvm-project/archive/llvmorg-${CLANG_VERSION}.tar.gz -o llvm.tar.gz
tar xf llvm.tar.gz && rm llvm.tar.gz
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
