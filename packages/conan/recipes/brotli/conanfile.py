# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/brotli/all/conanfile.py

from conan import ConanFile

class SystemBrotliConan(ConanFile):
    name = "brotli"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        includedir = "/usr/include/brotli"
        self.cpp_info.includedirs = [includedir]

        self.cpp_info.set_property("cmake_file_name", "brotli")
        self.cpp_info.set_property("cmake_target_name", "brotli::brotli")

        # brotlicommon
        self.cpp_info.components["brotlicommon"].includedirs = [includedir]
        self.cpp_info.components["brotlicommon"].system_libs = ["brotlicommon"]

        # brotlidec
        self.cpp_info.components["brotlidec"].includedirs = [includedir]
        self.cpp_info.components["brotlidec"].system_libs = ["brotlidec"]
        self.cpp_info.components["brotlidec"].requires = ["brotlicommon"]

        # brotlienc
        self.cpp_info.components["brotlienc"].includedirs = [includedir]
        self.cpp_info.components["brotlienc"].system_libs = ["brotlienc"]
        self.cpp_info.components["brotlienc"].requires = ["brotlicommon"]



