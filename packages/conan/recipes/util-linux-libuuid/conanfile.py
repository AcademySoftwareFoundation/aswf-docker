# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile

class SystemUtilLinuxLibuuidConan(ConanFile):
    name = "util-linux-libuuid"
    version = "wrapper"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
        self.cpp_info.libs = ["uuid"]
        
        self.cpp_info.set_property("cmake_file_name", "libuuid")
        self.cpp_info.set_property("cmake_target_name", "libuuid::libuuid")
