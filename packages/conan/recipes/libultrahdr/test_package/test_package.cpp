/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/b9c8a5391082c2940205ec80a619ec01b157fb59/recipes/libultrahdr/all/test_package/test_package.cpp
*/

#include <ultrahdr_api.h>
#include <iostream>

int main()
{
    uhdr_codec_private_t* decoder = uhdr_create_decoder();
    std::cout << "Creating new decoder " << decoder << "\n";
    std::cout << "Releasing decoder " << "\n";
    uhdr_release_decoder(decoder);

    return 0;
}
