# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/libxshmfence/all/conanfile.py

from conan import ConanFile

class SystemLibxshmfenceConan(ConanFile):
    name = "libxshmfence"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.system_libs = ["xshmfence"]
