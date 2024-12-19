/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/openimageio/all/test_package/test_package.cpp
*/

#include <OpenImageIO/imagecache.h>

int main()
{
    std::cout << "OpenImageIO " << OIIO_VERSION_STRING << "\n";

    std::string formats = OIIO::get_string_attribute("format_list");
    std::cout << "Supported formats:\n" << formats << "\n";
}
