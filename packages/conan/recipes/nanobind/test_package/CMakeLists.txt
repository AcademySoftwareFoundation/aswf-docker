# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/75b9e9922496dc0acc2499df76f8f10601042b60/recipes/nanobind/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.20)
project(test_package CXX)
enable_testing()

set(Python_FIND_UNVERSIONED_NAMES FIRST)

find_package(Python REQUIRED COMPONENTS Development OPTIONAL_COMPONENTS Interpreter)
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(conan_test_package NB_STATIC test_package.cpp)

if (Python_Interpreter_FOUND)
    add_test(NAME import_module
             COMMAND ${Python_EXECUTABLE} ${PROJECT_SOURCE_DIR}/test_package.py)
    set_tests_properties(import_module PROPERTIES
                         ENVIRONMENT "PYTHONPATH=$<TARGET_FILE_DIR:conan_test_package>")
endif()
