# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/lz4/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.1)
project(test_package LANGUAGES C)

find_package(lz4 REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
if(TARGET LZ4::lz4_static)
    target_link_libraries(${PROJECT_NAME} PRIVATE LZ4::lz4_static)
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE LZ4::lz4_shared)
endif()

option(TEST_SHARED_LIB "Use package in a shared library")
if(TEST_AS_SHARED_LIB)
    add_library(${PROJECT_NAME}2 SHARED lib.c)
    if(TARGET LZ4::lz4_static)
        target_link_libraries(${PROJECT_NAME}2 PRIVATE LZ4::lz4_static)
    else()
        target_link_libraries(${PROJECT_NAME}2 PRIVATE LZ4::lz4_shared)
    endif()
endif()
