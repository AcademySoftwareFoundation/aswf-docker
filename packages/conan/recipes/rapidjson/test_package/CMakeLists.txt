# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/3c237f4a7e8f29eacae90b809e4f18e75dfc05a3/recipes/rapidjson/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package)

find_package(RapidJSON CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE rapidjson)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
