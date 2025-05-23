# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/tree/b96b04ffad873992cbcfb98f0d84f6f44beb169d/recipes/fmt/all/test_package

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(fmt REQUIRED CONFIG)

add_executable(test_package test_package.cpp)
target_compile_features(test_package PRIVATE cxx_std_14)
if(FMT_HEADER_ONLY)
    target_link_libraries(test_package PRIVATE fmt::fmt-header-only)
else()
    target_link_libraries(test_package PRIVATE fmt::fmt)
endif()

add_executable(test_ranges test_ranges.cpp)
target_compile_features(test_ranges PRIVATE cxx_std_14)
if(FMT_HEADER_ONLY)
    target_link_libraries(test_ranges PRIVATE fmt::fmt-header-only)
else()
    target_link_libraries(test_ranges PRIVATE fmt::fmt)
endif()
