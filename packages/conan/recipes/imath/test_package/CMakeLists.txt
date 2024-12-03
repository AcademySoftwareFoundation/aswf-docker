# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/cceee569179c10fa56d1fd9c3582f3371944ba59/recipes/imath/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.12)
project(test_package LANGUAGES CXX)

find_package(Imath REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} Imath::Imath)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
