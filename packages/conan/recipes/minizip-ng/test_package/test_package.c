/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/minizip-ng/all/test_package/test_package.c
*/

#include <stdlib.h>
#include <mz.h>
#include <mz_os.h>

int main(int argc, char** argv)
{
    char output[256];
    memset(output, 'z', sizeof(output));
    int32_t err = mz_path_resolve("c:\\test\\.", output, sizeof(output));
    int32_t ok = (strcmp(output, "c:\\test\\") == 0);
    return EXIT_SUCCESS;
}
