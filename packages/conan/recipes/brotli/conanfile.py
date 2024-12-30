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
        self.cpp_info.libdirs = ["/usr/lib64"]

        includedir = "/usr/include/brotli"
        self.cpp_info.set_property("cmake_file_name", "Brotli")
        self.cpp_info.set_property("cmake_target_name", "Brotli::Brotli")

        # brotlicommon
        self.cpp_info.components["brotlicommon"].includedirs.append(includedir)
        self.cpp_info.components["brotlicommon"].libs = ["brotlicommon"]

        # brotlidec
        self.cpp_info.components["brotlidec"].includedirs.append(includedir)
        self.cpp_info.components["brotlidec"].libs = ["brotlidec"]
        self.cpp_info.components["brotlidec"].requires = ["brotlicommon"]

        # brotlienc
        self.cpp_info.components["brotlienc"].includedirs.append(includedir)
        self.cpp_info.components["brotlienc"].libs = ["brotlienc"]
        self.cpp_info.components["brotlienc"].requires = ["brotlicommon"]



