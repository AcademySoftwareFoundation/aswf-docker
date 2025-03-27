/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/b96b04ffad873992cbcfb98f0d84f6f44beb169d/recipes/libjxl/all/test_package/test_package.c
*/

#include <stdio.h>
#include <stdlib.h>

#include "jxl/decode.h"
#include "jxl/thread_parallel_runner.h"

int main()
{
    JxlDecoder *dec = NULL;
    void *runner = NULL;
    dec = JxlDecoderCreate(NULL);

    // Allways True
    if (JxlDecoderSubscribeEvents(dec, JXL_DEC_BASIC_INFO) == JXL_DEC_SUCCESS)
    {
        printf("Test");
    }
}
