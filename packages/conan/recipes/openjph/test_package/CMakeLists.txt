# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5d3d03d17ad9f83e87f8cfc3b6a701352bb517cc/recipes/openjph/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.11)
project(test_package LANGUAGES CXX)

find_package(openjph REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE openjph::openjph)
