# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/pystring/all/CMakeLists.txt

cmake_minimum_required(VERSION 3.4)

project(pystring LANGUAGES CXX)

include(GNUInstallDirs)

add_library(pystring ${PYSTRING_SRC_DIR}/pystring.cpp)
set_property(TARGET pystring PROPERTY WINDOWS_EXPORT_ALL_SYMBOLS TRUE)

install(TARGETS pystring
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(FILES ${PYSTRING_SRC_DIR}/pystring.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
