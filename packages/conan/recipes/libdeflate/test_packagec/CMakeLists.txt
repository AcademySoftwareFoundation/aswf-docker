# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/187fd740e479c64303915954b5d43f56a490ce68/recipes/libdeflate/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES C)

find_package(libdeflate REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
if(TARGET libdeflate::libdeflate_static)
    target_link_libraries(${PROJECT_NAME} PRIVATE libdeflate::libdeflate_static)
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE libdeflate::libdeflate_shared)
endif()
