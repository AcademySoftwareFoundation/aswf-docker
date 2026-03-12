/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
*/

#include <OpenImageIO/imagecache.h>

int main()
{
    std::cout << "OpenImageIO " << OIIO_VERSION_STRING << "\n";

    std::string formats = OIIO::get_string_attribute("format_list");
    std::cout << "Supported formats:\n" << formats << "\n";
}
