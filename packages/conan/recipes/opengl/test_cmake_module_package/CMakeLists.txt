# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/4622ac85d1cec8cb7a2fcc8a1796d4b73bff285e/recipes/opengl/all/test_cmake_module_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.10)
project(test_package)

find_package(OpenGL REQUIRED)

set(SOURCES ../test_package/test_package.cpp)

if(WIN32)
    list(APPEND SOURCES ../test_package/win.cpp)
endif()

if(APPLE)
    list(APPEND SOURCES ../test_package/osx.mm)
    set_source_files_properties(../test_package/osx.mm PROPERTIES COMPILE_FLAGS "-x objective-c++")

    list(APPEND PLATFORM_LIBS "objc")

    find_library(APPKIT_LIBRARY AppKit)
    find_library(FOUNDATION_LIBRARY Foundation)

    if(APPKIT_LIBRARY)
        list(APPEND PLATFORM_LIBS ${APPKIT_LIBRARY})
    endif()

    if(FOUNDATION_LIBRARY)
        list(APPEND PLATFORM_LIBS ${FOUNDATION_LIBRARY})
    endif()
endif()

add_executable(${PROJECT_NAME} ${SOURCES})
target_link_libraries(${PROJECT_NAME} PRIVATE OpenGL::GL ${PLATFORM_LIBS})