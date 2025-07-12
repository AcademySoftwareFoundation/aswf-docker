# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/1729c3c2c3b0e9d058821fa00e8a54154415efc6/recipes/md4c/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES C)

find_package(md4c CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(test_package PRIVATE md4c::md4c)
