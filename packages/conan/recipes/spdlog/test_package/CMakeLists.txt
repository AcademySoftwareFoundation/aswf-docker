# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/06fb0be6b9ffe79c8e74eb9739bcef0545994bef/recipes/spdlog/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(spdlog REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
if(SPDLOG_HEADER_ONLY)
    target_link_libraries(${PROJECT_NAME} PUBLIC spdlog::spdlog_header_only)
else()
    target_link_libraries(${PROJECT_NAME} PUBLIC spdlog::spdlog)
endif()

if(SPDLOG_USE_STD_FORMAT)
    target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_20)
else()
    target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
endif()
