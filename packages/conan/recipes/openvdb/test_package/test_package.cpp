/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/47ec06eaf213b77bf96c28079434b4fe4446cc46/recipes/openvdb/all/test_package/test_package.cpp
*/

#include <openvdb/openvdb.h>
#include <iostream>

int main()
{
    openvdb::initialize();
    openvdb::FloatGrid::Ptr grid = openvdb::FloatGrid::create();
    openvdb::FloatGrid::Accessor accessor = grid->getAccessor();
    openvdb::Coord xyz(1000, -200000000, 30000000);
    accessor.setValue(xyz, 1.0);
    std::cout << "Grid" << xyz << " = " << accessor.getValue(xyz) << std::endl;
}
