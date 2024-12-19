/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/lcms/all/test_package/test_package.c
*/

#include "lcms2.h"

int main()
{
    cmsUInt16Number linear[2] = { 0, 0xffff };
    cmsToneCurve * curve = cmsBuildTabulatedToneCurve16(0, 2, linear);
    cmsFreeToneCurve(curve);
}
