# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/2a3cb93885141024c1b405a01a79fb3abc239b12/recipes/ptex/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.1)
project(test_package LANGUAGES CXX)

find_package(ptex REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
if(TARGET Ptex::Ptex_static)
    target_link_libraries(${PROJECT_NAME} PRIVATE Ptex::Ptex_static)
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE Ptex::Ptex_dynamic)
endif()
