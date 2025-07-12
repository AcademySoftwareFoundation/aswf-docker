# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/pulseaudio/all/conanfile.py

from conan import ConanFile

class SystemPulseAudioConan(ConanFile):
    name = "pulseaudio"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = ["pulseaudio"]
        
        self.cpp_info.components["pulse"].system_libs = ["pulse", "pulsecommon-14.0"]

        self.cpp_info.components["pulse-simple"].system_libs = ["pulse-simple"]
        self.cpp_info.components["pulse-simple"].requires = ["pulse"]
