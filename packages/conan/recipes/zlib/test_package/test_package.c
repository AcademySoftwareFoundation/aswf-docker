/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/3375dfbcae9df4cee7b4eb6323b584fb60a2c8d0/recipes/zlib/all/test_package/test_package.c
*/

#include <stdlib.h>
#include <stdio.h>
#include <stdlib.h>

#include <zlib.h>

int main(void) {

    printf("ZLIB VERSION: %s\n", zlibVersion());

    return EXIT_SUCCESS;
}
