# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/vulkan-headers/all/conanfile.py

from conan import ConanFile

import os

class SystemVulkanHeadersConan(ConanFile):
    name = "vulkan-headers"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.system_libs = ["vulkan"]
        self.cpp_info.system_libs.extend(["dl", "pthread", "m"])

        self.cpp_info.set_property("cmake_file_name", "VulkanHeaders")
        self.cpp_info.components["vulkanheaders"].set_property("cmake_target_name", "Vulkan::Headers")
        self.cpp_info.components["vulkanheaders"].includedirs = ["/usr/include"]
        self.cpp_info.components["vulkanheaders"].bindirs = []
        self.cpp_info.components["vulkanheaders"].libdirs = []
        self.cpp_info.components["vulkanregistry"].set_property("cmake_target_name", "Vulkan::Registry")
        self.cpp_info.components["vulkanregistry"].includedirs = ["/usr/share/vulkan/registry"]
        self.cpp_info.components["vulkanregistry"].bindirs = []
        self.cpp_info.components["vulkanregistry"].libdirs = []
        self.cpp_info.components["vulkanregistry"].resdirs = ["res"]

