# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

# rawtoaces-config.cmake unconditionally emits find_dependency(nanobind).
# nanobind's own (unpatched) upstream cmake config never calls
# find_package(Python) itself -- it only checks that a Python::Module
# target already exists (created directly by Conan's cpython package's own
# generated CMake integration, via find_dependency(cpython) which runs
# first) and then reads the Python_EXECUTABLE/Python_VERSION *variables*.
# Since that target wasn't produced by a real find_package(Python) call,
# neither variable is actually populated, so nanobind's own
# `Python_VERSION VERSION_LESS "3.9"` check sees an empty version and its
# later Python_EXECUTABLE-based execute_process() calls would fail too.
# rawtoaces works around the Python_EXECUTABLE half of this in its own
# configure.cmake (see patches/*-cmake-lensfun-python3.diff), but that
# patch never runs for a downstream consumer like this test package, so
# both variables need to be set here too, before find_package(rawtoaces)
# below triggers the nanobind cascade.
find_package(Python3 COMPONENTS Interpreter REQUIRED)
if(NOT Python_EXECUTABLE AND Python3_EXECUTABLE)
    set(Python_EXECUTABLE "${Python3_EXECUTABLE}" CACHE FILEPATH "" FORCE)
endif()
if(NOT Python_VERSION)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -c
            "import sys; print('.'.join(map(str, sys.version_info[:3])))"
        OUTPUT_VARIABLE Python_VERSION
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
endif()

find_package(rawtoaces CONFIG REQUIRED)

add_executable(test_package test_package.cpp)
target_link_libraries(test_package PUBLIC rawtoaces::rawtoaces_core)
