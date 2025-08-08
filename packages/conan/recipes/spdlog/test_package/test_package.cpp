/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/tree/06fb0be6b9ffe79c8e74eb9739bcef0545994bef/recipes/spdlog/all/test_package
*/

#include <cstdlib>
#include "spdlog/spdlog.h"

#if defined __has_include
#  if __has_include ("spdlog/fmt/bundled/core.h")
#    error "bundled fmt within spdlog should not be present"
#  endif
#endif

int main(void) {
    spdlog::info("Welcome to spdlog version {}.{}.{}  !", SPDLOG_VER_MAJOR, SPDLOG_VER_MINOR, SPDLOG_VER_PATCH);
    return EXIT_SUCCESS;
}
