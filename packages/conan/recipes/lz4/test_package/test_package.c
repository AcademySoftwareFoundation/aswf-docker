/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/lz4/all/test_package/test_package.c
*/

// LZ4 trivial example : print Library version number
// Copyright : Takayuki Matsuoka & Yann Collet


#include <stdio.h>
#include "lz4.h"

int main(int argc, char** argv)
{
	(void)argc; (void)argv;
    printf("Hello World ! LZ4 Library version = %d\n", LZ4_versionNumber());
    return 0;
}
