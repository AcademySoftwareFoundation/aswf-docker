/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/zstd/all/test_package/test_package.c
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zstd.h>

int main() {
    const char* originalData = "Sample text";
    size_t compressedSize = ZSTD_compressBound(strlen(originalData) + 1);
    printf("%zu\n", compressedSize);

    return 0;
}
