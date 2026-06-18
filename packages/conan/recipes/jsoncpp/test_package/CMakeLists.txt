# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/17720e2ac26d8cc280079e364c1563c460c5df31/recipes/jsoncpp/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.8)
project(test_package LANGUAGES CXX)

find_package(jsoncpp REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE JsonCpp::JsonCpp)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
