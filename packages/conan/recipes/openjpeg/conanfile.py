# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/openjpeg/all/conanfile.py

from conan import ConanFile
from conan.tools.files import load
import re
from packaging.version import Version

class SystemOpenjpegConan(ConanFile):
    name = "openjpeg"
    settings = "os", "arch", "compiler", "build_type"

    def set_version(self):
        content = load(self, "/usr/lib64/pkgconfig/libopenjp2.pc")
        match = re.search(r"^Version:\s*(.+)$", content, re.MULTILINE)
        self.version = match.group(1).strip()
   
    def package_info(self):
        v = Version(self.version)
        self.cpp_info.includedirs = [f"/usr/include/openjpeg-{v.major}.{v.minor}"]
        self.cpp_info.system_libs = ["openjp2"]
        
        self.cpp_info.set_property("cmake_file_name", "OpenJPEG")
        self.cpp_info.set_property("cmake_target_name", "openjpeg::openjpeg")
