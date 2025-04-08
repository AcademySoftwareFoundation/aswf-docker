# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/b8bd958a29ef769d74a40471f1ada0426d1f8fff/recipes/tsl-robin-map/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(tsl-robin-map REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE tsl::robin_map)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
