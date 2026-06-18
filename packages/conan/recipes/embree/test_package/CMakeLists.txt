# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.8)
project(test_package LANGUAGES CXX)

find_package(embree4 REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE embree4)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
