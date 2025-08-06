/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/bad5c95b810e859c1c31553b92584246fe436d69/recipes/harfbuzz/all/test_package/test_package.c
*/

#include <stdio.h>
#include <string.h>
#include <hb.h>

int main() {
    const char *version = hb_version_string();
    printf("harfbuzz version: %s\n", version);
    return 0;
}
