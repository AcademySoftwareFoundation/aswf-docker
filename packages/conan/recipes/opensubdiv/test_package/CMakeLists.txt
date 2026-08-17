# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/2a3cb93885141024c1b405a01a79fb3abc239b12/recipes/opensubdiv/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(OpenSubdiv REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
# ASWF: match camelCase from target names used in OpenSubdiv CMakeLists.txt
if(TARGET OpenSubdiv::osdCPU_static)
    target_link_libraries(${PROJECT_NAME} PRIVATE OpenSubdiv::osdCPU_static)
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE OpenSubdiv::osdCPU)
endif()
