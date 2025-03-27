# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/libwebp/all/conanfile.py

from conan import ConanFile

class SystemLibwebpConan(ConanFile):
    name = "libwebp"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
        
        self.cpp_info.set_property("cmake_file_name", "WebP")

        # webpdecoder
        self.cpp_info.components["webpdecoder"].libdirs = ["/usr/lib64"]
        self.cpp_info.components["webpdecoder"].set_property("cmake_target_name", "WebP::webpdecoder")
        self.cpp_info.components["webpdecoder"].libs = ["webpdecoder"]

        # webp
        self.cpp_info.components["webp"].libdirs = ["/usr/lib64"]
        self.cpp_info.components["webp"].set_property("cmake_target_name", "WebP::webp")
        self.cpp_info.components["webp"].libs = ["webp"]

        # webpdemux
        self.cpp_info.components["webpdemux"].libdirs = ["/usr/lib64"]
        self.cpp_info.components["webpdemux"].set_property("cmake_target_name", "WebP::webpdemux")
        self.cpp_info.components["webpdemux"].libs = ["webpdemux"]
        self.cpp_info.components["webpdemux"].requires = ["webp"]

        # webpmux
        self.cpp_info.components["webpmux"].libdirs = ["/usr/lib64"]
        self.cpp_info.components["webpmux"].set_property("cmake_target_name", "WebP::webpmux")
        self.cpp_info.components["webpmux"].libs = ["webpmux"]
        self.cpp_info.components["webpmux"].requires = ["webp"]
