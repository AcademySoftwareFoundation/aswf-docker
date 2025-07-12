# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/pcre2/all/conanfile.py

from conan import ConanFile

class SystemPCRE2Conan(ConanFile):
    name = "pcre2"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = []
        
        self.cpp_info.set_property("cmake_file_name", "PCRE2")
        self.cpp_info.components["pcre2-8"].set_property("cmake_target_name", "PCRE2::8BIT")
        self.cpp_info.components["pcre2-8"].system_libs = ["pcre2-8"]
        self.cpp_info.components["pcre2-posix"].set_property("cmake_target_name", "PCRE2::POSIX")
        self.cpp_info.components["pcre2-posix"].system_libs = ["pcre2-posix"]


