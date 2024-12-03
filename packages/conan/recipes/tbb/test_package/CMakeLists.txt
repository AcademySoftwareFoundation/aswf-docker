# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/cceee569179c10fa56d1fd9c3582f3371944ba59/recipes/onetbb/2020.x/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package CXX)

find_package(TBB REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} TBB::tbb)
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 11)
