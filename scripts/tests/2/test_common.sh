#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

clang_v=`clang --version`
if [[ $clang_v != clang\ version\ 10.0* ]]
then
    exit 1
fi

gcc_v=`gcc --version`
if [[ $gcc_v != gcc\ \(GCC\)\ 9.3* ]]
then
    exit 1
fi

ninja_v=`ninja --version`
if [[ $ninja_v != 1.* ]]
then
    exit 1
fi

git_v=`git --version`
if [[ $git_v != 2.* ]]
then
    exit 1
fi

