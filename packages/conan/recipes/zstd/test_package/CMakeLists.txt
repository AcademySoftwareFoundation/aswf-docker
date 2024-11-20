# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/zstd/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.1)
project(test_package LANGUAGES C)

find_package(zstd REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
if (TARGET zstd::libzstd_shared)
    target_link_libraries(${PROJECT_NAME} PRIVATE zstd::libzstd_shared)
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE zstd::libzstd_static)
endif()
