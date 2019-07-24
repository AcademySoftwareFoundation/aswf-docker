#!/usr/bin/env bash

set -ex

# Temporary install of cmake for clang
curl --location "https://github.com/Kitware/CMake/releases/download/v3.12.4/cmake-3.12.4-Linux-x86_64.sh" -o /tmp/cmake.sh
mkdir /tmp/cmake && sh /tmp/cmake.sh --skip-license --prefix=/tmp/cmake --exclude-subdir
export PATH=/tmp/cmake/bin:$PATH

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

rm /tmp/cmake.sh
rm -rf /tmp/cmake
