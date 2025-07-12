# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/47ec06eaf213b77bf96c28079434b4fe4446cc46/recipes/openvdb/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package CXX)

find_package(OpenVDB REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE OpenVDB::openvdb)
if (OpenVDB_VERSION VERSION_GREATER_EQUAL "10.0.0")
    target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_17)
else()
    target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_14)
endif()
