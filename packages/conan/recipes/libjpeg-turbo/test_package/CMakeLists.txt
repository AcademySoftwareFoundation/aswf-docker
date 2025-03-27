# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/libjpeg-turbo/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES C)

find_package(libjpeg-turbo REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
if(TARGET libjpeg-turbo::jpeg)
    target_link_libraries(${PROJECT_NAME} PRIVATE libjpeg-turbo::jpeg)
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE libjpeg-turbo::jpeg-static)
endif()
target_compile_features(${PROJECT_NAME} PRIVATE c_std_99)
