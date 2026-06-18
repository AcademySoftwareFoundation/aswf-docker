# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/69a86578676209faf77da621e2f8efd3479c2e33/recipes/lua/all/CMakeLists.txt
#
# Originally taken from:
# https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/lua/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(lua)

option(COMPILE_AS_CPP "Compile Lua as C++" OFF)
option(SKIP_INSTALL_TOOLS "Skip installation of Lua interpreter and compiler" ON)
option(WITH_READLINE "Link Lua interpreter with readline" OFF)

SET(SOURCE_DIR ${LUA_SRC_DIR})

FILE(GLOB SRC_LIBLUA "${SOURCE_DIR}/src/*.c")
SET(SRC_LUAI "${SOURCE_DIR}/src/lua.c")
SET(SRC_LUAC "${SOURCE_DIR}/src/luac.c")
LIST(REMOVE_ITEM SRC_LIBLUA ${SRC_LUAC} ${SRC_LUAI})

IF(COMPILE_AS_CPP)
    SET_SOURCE_FILES_PROPERTIES(${SRC_LIBLUA} ${SRC_LUAI} ${SRC_LUAC}
        PROPERTIES LANGUAGE CXX)
ELSE()
    SET(CMAKE_C_STANDARD 99)
ENDIF()

IF(WIN32)
    ADD_DEFINITIONS(-D_CRT_SECURE_NO_WARNINGS)
ENDIF()

IF(UNIX)
    IF(NOT ANDROID)
        ADD_DEFINITIONS(-DLUA_USE_POSIX)
    ENDIF()
    FIND_LIBRARY(LIB_MATH NAMES m)
    IF(LIB_MATH)
        LINK_LIBRARIES(${LIB_MATH})
    ENDIF()
ENDIF()

ADD_LIBRARY(lua ${SRC_LIBLUA})

IF(COMPILE_AS_CPP)
    SET_TARGET_PROPERTIES(lua PROPERTIES OUTPUT_NAME "lua-c++")
ENDIF()

IF(BUILD_SHARED_LIBS AND WIN32)
    TARGET_COMPILE_DEFINITIONS(lua PUBLIC -DLUA_BUILD_AS_DLL)
ENDIF()

IF(UNIX)
    IF(APPLE)
        TARGET_COMPILE_DEFINITIONS(lua PUBLIC -DLUA_USE_DLOPEN)
    ELSE()
        FIND_LIBRARY(LIB_DLOPEN NAMES dl)
        IF(LIB_DLOPEN)
            TARGET_LINK_LIBRARIES(lua ${LIB_DLOPEN})
            TARGET_COMPILE_DEFINITIONS(lua PUBLIC -DLUA_USE_DLOPEN)
        ENDIF()
    ENDIF()
ENDIF()

INCLUDE(GNUInstallDirs)
INSTALL(TARGETS lua
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})

IF(NOT SKIP_INSTALL_TOOLS)
    ADD_EXECUTABLE(luac ${SRC_LUAC} ${SRC_LIBLUA})
    ADD_EXECUTABLE(luai ${SRC_LUAI})
    TARGET_LINK_LIBRARIES(luai lua)
    SET_TARGET_PROPERTIES(luai PROPERTIES OUTPUT_NAME lua PDB_NAME luai)
    IF(WITH_READLINE)
        find_package(readline REQUIRED CONFIG)
        TARGET_COMPILE_DEFINITIONS(luai PUBLIC -DLUA_USE_READLINE)
        TARGET_LINK_LIBRARIES(luai readline::readline)
    ENDIF()
    INSTALL(TARGETS luai luac RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
ENDIF()

INSTALL(
    FILES
        ${SOURCE_DIR}/src/lualib.h
        ${SOURCE_DIR}/src/lua.h
        ${SOURCE_DIR}/src/luaconf.h
        ${SOURCE_DIR}/src/lauxlib.h
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
IF(NOT COMPILE_AS_CPP)
    INSTALL(FILES ${SOURCE_DIR}/src/lua.hpp DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
ENDIF()
