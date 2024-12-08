# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/2a3cb93885141024c1b405a01a79fb3abc239b12/recipes/materialx/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)

project(test_package  LANGUAGES CXX)

find_package(materialx REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE materialx::MaterialXCore materialx::MaterialXFormat)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_14)
