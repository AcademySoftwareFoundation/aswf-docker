/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/opencolorio/all/test_package/test_package.cpp
*/

#include <OpenColorIO/OpenColorIO.h>
#include <iostream>

int main()
{
    std::cout << "OpenColorIO " << OCIO_NAMESPACE::GetVersion() << "\n";
    return 0;
}
