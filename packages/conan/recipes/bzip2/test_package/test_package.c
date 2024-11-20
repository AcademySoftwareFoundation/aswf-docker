/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5fecff85282c68fae05e776fb330779bdb94a6e8/recipes/bzip2/all/test_package/test_package.c
*/

#include <stdio.h>
#include <stdlib.h>
#include "bzlib.h"


int main(void) {
    char buffer [256] = {0};
    unsigned int size = 256;
    const char* version = BZ2_bzlibVersion();
    printf("Bzip2 version: %s\n", version);
    BZ2_bzBuffToBuffCompress(buffer, &size, "conan-package-manager", 21, 1, 0, 1);
    printf("Bzip2 compressed: %s\n", buffer);
    return EXIT_SUCCESS;
}
