# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile

class SystemXkbcommonConan(ConanFile):
    name = "xkbcommon"
    version = "wrapper"
    
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "with_x11": [True, False],
    }
    default_options = {
        "with_x11": True,
    }
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
        
        self.cpp_info.components["libxkbcommon"].libs = ["xkbcommon"]
        self.cpp_info.components["libxkbcommon-x11"].libs = ["xkbcommon-x11"]
