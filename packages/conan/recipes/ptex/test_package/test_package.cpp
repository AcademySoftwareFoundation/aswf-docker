/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/2a3cb93885141024c1b405a01a79fb3abc239b12/recipes/ptex/all/test_package/test_package.cpp
*/

#include <Ptexture.h>

int main() {
    PtexPtr<PtexCache> c(PtexCache::create(0, 1024 * 1024));
    return 0;
}
