# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/8439f2704e151c2e7c7b55994c7046f8aefa1270/recipes/lcms/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES C)

find_package(lcms REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(${PROJECT_NAME} PRIVATE lcms::lcms)
