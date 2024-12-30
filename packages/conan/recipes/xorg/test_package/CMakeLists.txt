# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/4622ac85d1cec8cb7a2fcc8a1796d4b73bff285e/recipes/xorg/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.1)
project(test_package LANGUAGES C)

find_package(xorg REQUIRED CONFIG)

add_executable(test_package test_package.c)
target_link_libraries(test_package PRIVATE xorg::xorg)