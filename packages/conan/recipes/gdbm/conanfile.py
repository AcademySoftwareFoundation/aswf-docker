# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile

class SystemGdbmConan(ConanFile):
    name = "gdbm"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.system_libs = ["gdbm", "gdbm_compat"]
        
        self.cpp_info.set_property("cmake_file_name", "gdbm")
        self.cpp_info.set_property("cmake_target_name", "gdbm::gdbm")
