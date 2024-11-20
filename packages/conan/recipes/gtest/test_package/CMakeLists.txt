# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/gtest/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.8)
project(test_package LANGUAGES CXX)

find_package(GTest REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE GTest::gtest)
if(GTest_VERSION VERSION_LESS "1.13.0")
    target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
else()
    target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_14)
endif()

if(WITH_MAIN)
    target_link_libraries(${PROJECT_NAME} PRIVATE GTest::gtest_main)
    if(WITH_GMOCK)
        target_link_libraries(${PROJECT_NAME} PRIVATE GTest::gmock_main)
    endif()
else()
    target_sources(${PROJECT_NAME} PRIVATE main.cpp)
endif()

if(WITH_GMOCK)
    target_link_libraries(${PROJECT_NAME} PRIVATE GTest::gmock)
    target_compile_definitions(${PROJECT_NAME} PRIVATE WITH_GMOCK)
endif()
