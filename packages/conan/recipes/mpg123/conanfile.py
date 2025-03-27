# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/mpg123/all/conanfile.py

from conan import ConanFile

class SystemMpg123Conan(ConanFile):
    name = "mpg123"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]

        self.cpp_info.set_property("cmake_file_name", "mpg123")
        
        self.cpp_info.components["libmpg123"].libs = ["mpg123"]
        self.cpp_info.components["libmpg123"].set_property("cmake_target_name", "MPG123::libmpg123")

        self.cpp_info.components["libout123"].libs = ["out123"]
        self.cpp_info.components["libout123"].set_property("cmake_target_name", "MPG123::libout123")
        self.cpp_info.components["libout123"].requires = ["libmpg123"]

        self.cpp_info.components["libsyn123"].libs = ["syn123"]
        self.cpp_info.components["libsyn123"].set_property("cmake_target_name", "MPG123::libsyn123")
        self.cpp_info.components["libsyn123"].requires = ["libmpg123"]
