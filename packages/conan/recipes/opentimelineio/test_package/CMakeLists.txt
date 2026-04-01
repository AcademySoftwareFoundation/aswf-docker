# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/EstebanDugueperoux2/conan-center-index/blob/1d8986d11305e1303b1581532f327cdd9d32ed20/recipes/openusd/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)

project(test_package LANGUAGES CXX)

find_package(OpenTimelineIO REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE OpenTimelineIO::OpenTimelineIO)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_17)
