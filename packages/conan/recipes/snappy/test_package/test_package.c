/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From:https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/snappy/all/test_package/test_package.c
*/

#include <snappy-c.h>

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    const char *input = "conan-center-index";
    size_t input_length = strlen(input);
    size_t output_length = snappy_max_compressed_length(input_length);
    char *output = (char*)malloc(output_length);
    if (output == NULL) return 0;
    if (snappy_compress(input, input_length, output, &output_length) == SNAPPY_OK) {
        printf("%s compressed: %s\n", input, output);
    }
    free(output);
    return 0;
}
