# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/vorbis/all/conanfile.py

from conan import ConanFile

class SystemVorbisConan(ConanFile):
    name = "vorbis"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
        
        self.cpp_info.set_property("cmake_file_name", "Vorbis")

        # vorbis
        self.cpp_info.components["vorbismain"].set_property("cmake_target_name", "Vorbis::vorbis")
        self.cpp_info.components["vorbismain"].libs = ["vorbis"]

        # vorbisenc
        self.cpp_info.components["vorbisenc"].set_property("cmake_target_name", "Vorbis::vorbisenc")
        self.cpp_info.components["vorbisenc"].libs = ["vorbisenc"]

        # vorbisfile
        self.cpp_info.components["vorbisfile"].set_property("cmake_target_name", "Vorbis::vorbisfile")
        self.cpp_info.components["vorbisfile"].libs = ["vorbisfile"]

