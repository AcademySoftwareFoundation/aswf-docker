# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/bad5c95b810e859c1c31553b92584246fe436d69/recipes/harfbuzz/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.8)
project(test_package LANGUAGES C)

find_package(harfbuzz REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(${PROJECT_NAME} PRIVATE harfbuzz::harfbuzz)
target_compile_features(${PROJECT_NAME} PRIVATE c_std_99)
