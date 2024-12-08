# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/cceee569179c10fa56d1fd9c3582f3371944ba59/recipes/openexr/3.x/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.8)
project(test_package LANGUAGES CXX)

find_package(OpenEXR REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE OpenEXR::OpenEXR)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
