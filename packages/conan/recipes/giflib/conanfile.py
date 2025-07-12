# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/giflib/5.1.x/conanfile.py

from conan import ConanFile
from conan.tools.files import load
from io import StringIO

class SystemGiflibConan(ConanFile):
    name = "giflib"
    settings = "os", "arch", "compiler", "build_type"

    def set_version(self):
        # giflib-devel missing a pkgconfig on RHEL
        cmd = "rpm -q --qf '%{VERSION}' giflib-devel"
        stdout = StringIO()
        self.run(cmd, stdout=stdout)
        self.version = stdout.getvalue()

    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
        self.cpp_info.libs = ["gif"]
        
        self.cpp_info.set_property("cmake_file_name", "GIF")
        self.cpp_info.set_property("cmake_target_name", "GIF::GIF")
