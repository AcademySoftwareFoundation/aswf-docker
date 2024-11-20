# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/22dfbd2b42eed730eca55e14025e8ffa65f723b2/recipes/log4cplus/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.8)
project(test_package LANGUAGES CXX)

find_package(log4cplus REQUIRED CONFIG)

if(log4cplus_VERSION VERSION_GREATER_EQUAL 2)
    add_executable(${PROJECT_NAME} test_package.cpp)
else()
    add_executable(${PROJECT_NAME} test_package_v1.cpp)
endif()
target_link_libraries(${PROJECT_NAME} PRIVATE log4cplus::log4cplus)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
