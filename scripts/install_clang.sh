#!/usr/bin/env bash

set -ex

CLANG_VERSION="$1"

git clone https://github.com/llvm/llvm-project.git
cd llvm-project

if [ "$CLANG_VERSION" != "latest" ]; then
    git checkout tags/llvmorg-${CLANG_VERSION} -b llvmorg-${CLANG_VERSION}
fi

mkdir build
cd build
cmake -DLLVM_ENABLE_PROJECTS=clang -G "Unix Makefiles" ../llvm
make -j4
make install

cd ../..
rm -rf llvm-project
