# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/59cab50aa90f922e61a746eef7c488dd788e4989/recipes/pybind11/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)
enable_testing()

find_package(Python3 REQUIRED COMPONENTS Development OPTIONAL_COMPONENTS Interpreter)
find_package(pybind11 REQUIRED CONFIG)

pybind11_add_module(test_package MODULE test_package.cpp)
set_property(TARGET test_package PROPERTY CXX_STANDARD 11)

if (Python_Interpreter_FOUND)
    add_test(NAME import_module
             COMMAND ${Python_EXECUTABLE} ${PROJECT_SOURCE_DIR}/test.py)
    set_tests_properties(import_module PROPERTIES
                         ENVIRONMENT "PYTHONPATH=$<TARGET_FILE_DIR:test_package>")
endif()
