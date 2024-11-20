/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/lz4/all/test_package/lib.c
*/

#include "lz4.h"

#ifdef _MSC_VER
#define API __declspec(dllexport)
#else
#define API __attribute__ ((visibility("default")))
#endif

API
int lz4_version()
{
    return LZ4_versionNumber();
}
