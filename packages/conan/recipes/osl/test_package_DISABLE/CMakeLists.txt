# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#

cmake_minimum_required(VERSION 3.15)
project(test_package CXX)

find_package(OpenShadingLanguage REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
# ASWF: when building test package, Conan package name is part of target
target_link_libraries(${PROJECT_NAME} PRIVATE osl::OpenImageIO )
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_14)
