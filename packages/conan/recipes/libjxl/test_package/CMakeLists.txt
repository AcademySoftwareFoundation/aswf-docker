# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/b96b04ffad873992cbcfb98f0d84f6f44beb169d/recipes/libjxl/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package C)

find_package(libjxl REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(${PROJECT_NAME} PRIVATE libjxl::libjxl)
