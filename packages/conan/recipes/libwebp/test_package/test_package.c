/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f2c56e90ae28fef1ee1a392adf59f96199ee1277/recipes/libwebp/all/test_package/test_package.c
*/

#include <stdio.h>
#include <webp/decode.h>

int main(void)
{
    int version = WebPGetDecoderVersion();
    printf("Webp Decoder version: %d\n", version);

    return 0;
}
