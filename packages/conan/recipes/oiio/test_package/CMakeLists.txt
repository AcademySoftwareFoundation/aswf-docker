# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/openimageio/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package CXX)

find_package(OpenImageIO REQUIRED CONFIG)
find_package(fmt REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
# ASWF: when building test package, Conan package name is part of target
target_link_libraries(${PROJECT_NAME} PRIVATE oiio::OpenImageIO
                                              oiio::OpenImageIO_Util
                                              fmt::fmt)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_14)
