# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/libsvtav1/all/conanfile.py

from conan import ConanFile

class SystemSVTAV1Conan(ConanFile):
    name = "libsvtav1"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]

        self.cpp_info.components["encoder"].libs = ["SvtAv1Enc"]
        self.cpp_info.components["encoder"].includedirs = ["/usr/include/svt-av1"]
        self.cpp_info.components["decoder"].libs = ["SvtAv1Dec"]
        self.cpp_info.components["decoder"].includedirs = ["/usr/include/svt-av1"]
