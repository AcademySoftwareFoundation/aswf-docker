# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/4622ac85d1cec8cb7a2fcc8a1796d4b73bff285e/recipes/tcl/all/conanfile.py

from conan import ConanFile

class SystemTclConan(ConanFile):
    name = "tcl"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
        self.cpp_info.libs = ["tcl"]
        
        self.cpp_info.set_property("cmake_file_name", "TCL")
        self.cpp_info.set_property("cmake_target_name", "TCL::TCL")
