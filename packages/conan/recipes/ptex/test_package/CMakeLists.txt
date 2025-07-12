# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/d8323e1d365e32d88042e5070a483fc55a337856/recipes/ptex/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(ptex REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
if(TARGET Ptex::Ptex_static)
    target_link_libraries(${PROJECT_NAME} PRIVATE Ptex::Ptex_static)
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE Ptex::Ptex_dynamic)
endif()
