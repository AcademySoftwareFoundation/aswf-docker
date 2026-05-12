# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/8abb942c5fb4acd481548950143024fdcf29ef8f/recipes/qt/5.x.x/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.8)
project(test_package LANGUAGES CXX)

find_package(Qt5 COMPONENTS Core Network Sql Concurrent Xml REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp greeter.h example.qrc)
target_link_libraries(${PROJECT_NAME} PRIVATE Qt5::Core Qt5::Network Qt5::Sql Qt5::Concurrent Qt5::Xml)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
set_target_properties(${PROJECT_NAME} PROPERTIES AUTOMOC ON AUTORCC ON)
