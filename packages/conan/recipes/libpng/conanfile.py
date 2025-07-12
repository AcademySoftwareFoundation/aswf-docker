# Copyright (c) Contributors to the conan-center-index Project. All rights reserved. 
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/libpng/all/conanfile.py

from conan import ConanFile
from conan.tools.files import load
import re

class SystemLibpngConan(ConanFile):
    name = "libpng"
    
    settings = "os", "arch", "compiler", "build_type"

    def set_version(self):
        content = load(self, "/usr/lib64/pkgconfig/libpng.pc")
        match = re.search(r"^Version:\s*(.+)$", content, re.MULTILINE)
        self.version = match.group(1).strip()
   
    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.system_libs = ["png"]
        
        self.cpp_info.set_property("cmake_file_name", "PNG")
        self.cpp_info.set_property("cmake_target_name", "PNG::PNG")
