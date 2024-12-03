/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/cceee569179c10fa56d1fd9c3582f3371944ba59/recipes/imath/all/test_package/test_package.cpp
*/

#include <Imath/half.h>
#include <iostream>

int main(int argc, char *argv[])
{
    std::cout << half(1.0) << "\n";
    return 0;
}
