/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/c29c3a06d0c5d4fd98529a34586c4f60ab00f659/recipes/onetbb/all/test_package/test_package.cpp
*/

#include <tbb/tbb.h>
#include <iostream>

int main(){
    std::cout << "tbb runtime version: " << TBB_runtime_version() << "\n";
    std::cout << "tbb runtime interface version: " << TBB_runtime_interface_version() << "\n";
    return 0;
}
