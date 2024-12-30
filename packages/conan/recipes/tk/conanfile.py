# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/4622ac85d1cec8cb7a2fcc8a1796d4b73bff285e/recipes/tk/all/conanfile.py

import os

from conan import ConanFile

class SystemTkConan(ConanFile):
    name = "tk"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"

    def requirements(self):
      self.requires(f"tcl/{self.version}@{os.environ['ASWF_PKG_ORG']}/{os.environ['ASWF_CONAN_CHANNEL']}", transitive_headers=True, transitive_libs=True)
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
        self.cpp_info.libs = ["tk"]
        self.cpp_info.requires = ["tcl::tcl"]
        
        self.cpp_info.set_property("cmake_file_name", "TK")
        self.cpp_info.set_property("cmake_target_name", "TK::TK")
