# Copyright (c) Contributors to the OpenFX Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
#
# From: https://github.com/AcademySoftwareFoundation/openfx/blob/158c8b69d9a2016755696138e027fdfd71bab552/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(openfx CONFIG REQUIRED)

add_executable(test_package test_package.cpp)
target_link_libraries(test_package PUBLIC openfx::openfx)
