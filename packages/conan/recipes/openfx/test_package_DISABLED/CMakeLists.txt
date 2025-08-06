# Copyright (c) Contributors to the OpenFX Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
#
# From: https://github.com/AcademySoftwareFoundation/openfx/blob/158c8b69d9a2016755696138e027fdfd71bab552/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(openfx CONFIG REQUIRED)

add_executable(test_package src/test_package.cpp)
target_include_directories(test_package PUBLIC ${openfx_INCLUDE_DIRS})
target_link_libraries(test_package openfx::HostSupport)

# get_target_property(EXAMPLES_DIR openfx::Examples INTERFACE_CMAKE_EXAMPLES_DIR)
get_target_property(EXAMPLES_DIR openfx EXAMPLES_DIR)

file(GLOB_RECURSE PLUGIN_SOURCES "${EXAMPLES_DIR}/Invert/*.cpp")
message(STATUS "EXAMPLES_DIR value is: ${EXAMPLES_DIR}")
message(STATUS "openfx_DIR value is: ${openfx_DIR}")
message(STATUS "openfx_CONFIG value is: ${openfx_CONFIG}")

add_ofx_plugin(invert_plugin ${EXAMPLES_DIR}/Invert)
target_sources(invert_plugin PUBLIC ${PLUGIN_SOURCES})
target_include_directories(invert_plugin PUBLIC ${openfx_INCLUDE_DIRS})
target_link_libraries(invert_plugin openfx::Support)
