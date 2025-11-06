/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5d3d03d17ad9f83e87f8cfc3b6a701352bb517cc/recipes/openjph/all/test_package/test_package.cpp
*/

#include <openjph/ojph_arch.h>
#include <openjph/ojph_version.h>

#include <iostream>


int main() {
    // Print the version number but also do an API call to check the library
    std::cout << "OpenJPH Version: " << OPENJPH_VERSION_MAJOR << '.' << OPENJPH_VERSION_MINOR << '.' << OPENJPH_VERSION_PATCH << std::endl;
    std::cout << "CPU Extension level: " << ojph::get_cpu_ext_level() << std::endl;

    return EXIT_SUCCESS;
}
