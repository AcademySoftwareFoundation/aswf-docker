# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile

class SystemGdbmConan(ConanFile):
    name = "gdbm"
    version = "wrapper"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
        self.cpp_info.libs = ["gdbm", "gdbm_compat"]
        
        self.cpp_info.set_property("cmake_file_name", "gdbm")
        self.cpp_info.set_property("cmake_target_name", "gdbm::gdbm")
