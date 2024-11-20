/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/22dfbd2b42eed730eca55e14025e8ffa65f723b2/recipes/glew/all/test_package/test_package.c
*/

#include <GL/glew.h>

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

int main ()
{
    assert(glewGetString(GLEW_VERSION));
    printf("GLEW %s\n", glewGetString(GLEW_VERSION));
    return EXIT_SUCCESS;
}
