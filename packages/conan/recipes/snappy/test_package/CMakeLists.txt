# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/master/recipes/snappy/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.8)
project(test_package)

find_package(Snappy REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE Snappy::snappy)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)

add_executable(${PROJECT_NAME}_c test_package.c)
target_link_libraries(${PROJECT_NAME}_c PRIVATE Snappy::snappy)
