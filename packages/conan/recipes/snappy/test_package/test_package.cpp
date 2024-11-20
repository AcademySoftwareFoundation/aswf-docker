/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/snappy/all/test_package/test_package.cpp
*/

#include <snappy.h>

#include <cstdlib>
#include <string>
#include <iostream>

int main() {
    std::string input("conan-enter-index");
    std::string output;

    const size_t result = snappy::Compress(input.c_str(), input.size(), &output);

    std::cout << input << " compressed (" << result << "): " << output << std::endl;

    return EXIT_SUCCESS;
}
