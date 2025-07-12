# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile

class SystemMpdecimalConan(ConanFile):
    name = "mpdecimal"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.systemlibs = ["mpdec"]
        
        self.cpp_info.set_property("cmake_file_name", "mpdecimal")
        self.cpp_info.set_property("cmake_target_name", "mpdecimal::mpdecimal")
