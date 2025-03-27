/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/b96b04ffad873992cbcfb98f0d84f6f44beb169d/recipes/fmt/all/test_package/test_ranges.cpp
*/

#include <cstdlib>
#include <vector>
#include "fmt/ranges.h"

int main() {
    std::vector<char> numbers;
    fmt::format_to(std::back_inserter(numbers), "{}{}{}", 1, 2, 3);
    const std::string str_numbers = fmt::format("{}", numbers);
    fmt::print("numbers: {}\n", str_numbers);
    return EXIT_SUCCESS;
}
