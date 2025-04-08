/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/187fd740e479c64303915954b5d43f56a490ce68/recipes/libdeflate/all/test_package/test_package.c
*/

#include <libdeflate.h>

int main () {
    struct libdeflate_compressor *c;
    c = libdeflate_alloc_compressor(12);
    libdeflate_free_compressor(c);
    return 0;
}
