#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/llvmorg-${ASWF_CLANG_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/llvm/llvm-project/archive/llvmorg-${ASWF_CLANG_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/llvmorg-${ASWF_CLANG_VERSION}.tar.gz"
fi

tar xf "$DOWNLOADS_DIR/llvmorg-${ASWF_CLANG_VERSION}.tar.gz"
cd "llvm-project-llvmorg-${ASWF_CLANG_VERSION}/llvm"

mkdir build
cd build

if [[ $ASWF_CLANG_VERSION != 7.* && $ASWF_CLANG_VERSION != 8.* && $ASWF_CLANG_VERSION != 9.* && $ASWF_CLANG_VERSION != 10.* && $ASWF_CLANG_VERSION != 11.* ]]; then
    # Recent llvm requires python3 to build
    export PATH=/tmp/pytmp/bin:$PATH
    export LD_LIBRARY_PATH=/tmp/pytmp/lib:$LD_LIBRARY_PATH
    ASWF_INSTALL_PREFIX=/tmp/pytmp ASWF_PYTHON_VERSION=3.9.15 ASWF_NUMPY_VERSION=1.20 /tmp/build_python.sh
fi

if [[ $ASWF_CLANG_VERSION == 13.* || $ASWF_CLANG_VERSION == 14.* ]]; then
llvm_projects="clang;clang-tools-extra;compiler-rt;lld"
else
llvm_projects="clang;clang-tools-extra;libcxx;libcxxabi;compiler-rt;lld"
fi

cmake -DLLVM_ENABLE_PROJECTS=${llvm_projects} \
      -DCMAKE_BUILD_TYPE=Release \
      -G "Unix Makefiles" \
      -DGCC_INSTALL_PREFIX="/opt/rh/devtoolset-${ASWF_DTS_VERSION}/root/usr" \
      -DLLVM_TARGETS_TO_BUILD="host;NVPTX" \
      -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
      -DCLANG_INCLUDE_DOCS=OFF \
      -DLIBCXX_INCLUDE_DOCS=OFF \
      -DLLVM_BUILD_TESTS=OFF \
      -DLLVM_INCLUDE_TESTS=OFF \
      -DLLVM_INCLUDE_TOOLS=ON \
      -DLLVM_BUILD_TOOLS=ON \
      -DLLVM_TOOL_LLVM_AR_BUILD=OFF \
      -DLLVM_TOOL_LLVM_AS_BUILD=ON \
      -DLLVM_TOOL_LLVM_AS_FUZZER_BUILD=OFF \
      -DLLVM_TOOL_LLVM_BCANALYZER_BUILD=OFF \
      -DLLVM_TOOL_LLVM_COV_BUILD=OFF \
      -DLLVM_TOOL_LLVM_CXXDUMP_BUILD=OFF \
      -DLLVM_TOOL_LLVM_DIS_BUILD=OFF \
      -DLLVM_TOOL_LLVM_EXTRACT_BUILD=OFF \
      -DLLVM_TOOL_LLVM_C_TEST_BUILD=OFF \
      -DLLVM_TOOL_LLVM_DIFF_BUILD=OFF \
      -DLLVM_TOOL_LLVM_GO_BUILD=OFF \
      -DLLVM_TOOL_LLVM_JITLISTENER_BUILD=OFF \
      -DLLVM_TOOL_LLVM_LTO_BUILD=OFF \
      -DLLVM_TOOL_LLVM_MC_BUILD=OFF \
      -DLLVM_TOOL_LLVM_NM_BUILD=OFF \
      -DLLVM_TOOL_LLVM_OBJDUMP_BUILD=OFF \
      -DLLVM_TOOL_LLVM_BCANALYZER_BUILD=OFF \
      -DLLVM_TOOL_LLVM_PROFDATA_BUILD=OFF \
      -DLLVM_TOOL_LLVM_RTDYLD_BUILD=OFF \
      -DLLVM_TOOL_LLVM_SIZE_BUILD=OFF \
      -DLLVM_TOOL_LLVM_SPLIT_BUILD=OFF \
      -DLLVM_TOOL_LLVM_STRESS_BUILD=OFF \
      -DLLVM_TOOL_LLVM_SYMBOLIZER_BUILD=ON \
      -DLLVM_TOOL_LLVM_LTO_BUILD=OFF \
      -DLLVM_INCLUDE_EXAMPLES=OFF \
      ..

make -j$(nproc)
make install

cd ../../..
rm -rf "llvm-project-llvmorg-${ASWF_CLANG_VERSION}"
