# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5f19361f49bc31a349b383c1f95c7f79627f728a/recipes/jasper/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES C)

find_package(Jasper REQUIRED)

set(_custom_vars
    JASPER_FOUND
    JASPER_INCLUDE_DIR
    JASPER_LIBRARIES
    JASPER_VERSION_STRING
)
foreach(_custom_var ${_custom_vars})
if(DEFINED ${_custom_var})
    message(STATUS "${_custom_var}: ${${_custom_var}}")
else()
    message(FATAL_ERROR "${_custom_var} not defined")
endif()
endforeach()

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(${PROJECT_NAME} PRIVATE Jasper::Jasper)
