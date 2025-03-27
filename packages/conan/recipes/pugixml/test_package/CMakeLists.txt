# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/pugixml/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.1)
project(test_package LANGUAGES CXX)

find_package(pugixml REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE pugixml::pugixml)
