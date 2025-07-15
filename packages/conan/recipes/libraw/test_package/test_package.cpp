/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5aa8fda35e023ceeaefb5a670ae9c0c3ca4fdf25/recipes/libraw/all/test_package/test_package.cpp
*/

#include <libraw/libraw.h>
#include <iostream>

int main()
{
    std::cout << libraw_version() << "\n";
    return 0;
}
