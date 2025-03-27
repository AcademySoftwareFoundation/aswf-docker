# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/libjpeg-turbo/all/test_package_module/CMakeLists.txt

cmake_minimum_required(VERSION 3.8)
project(test_package LANGUAGES C)

find_package(JPEG REQUIRED)

add_executable(${PROJECT_NAME} ../test_package/test_package.c)
target_link_libraries(${PROJECT_NAME} PRIVATE JPEG::JPEG)
target_compile_features(${PROJECT_NAME} PRIVATE c_std_99)
