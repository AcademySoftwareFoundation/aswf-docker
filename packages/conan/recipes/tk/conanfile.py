# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

import os

from conan import ConanFile

class SystemTkConan(ConanFile):
    name = "tk"
    version = "wrapper"
    
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
