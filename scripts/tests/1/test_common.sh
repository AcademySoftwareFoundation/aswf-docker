#!/usr/bin/env bash

set -ex

clang_v=`clang --version`
if [[ $clang_v != clang\ version\ 7.0* ]]
then
    exit 1
fi

gcc_v=`gcc --version`
if [[ $gcc_v != gcc\ \(GCC\)\ 6.3* ]]
then
    exit 1
fi

ninja_v=`ninja --version`
if [[ $ninja_v != 1.* ]]
then
    exit 1
fi
