/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/libxcrypt/all/test_package/test_package.c
*/

#include "crypt.h"

#include <stdio.h>
int main()
{
    printf("preferred method: %s\n", crypt_preferred_method());
    return 0;
}
