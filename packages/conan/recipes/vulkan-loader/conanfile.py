# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/vulkan-loader/all/conanfile.py

from conan import ConanFile

class SystemVulkanLoaderConan(ConanFile):
    name = "vulkan-loader"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include/vulkan"]
        self.cpp_info.system_libs = ["vulkan"]
        self.cpp_info.system_libs.extend(["dl", "pthread", "m"])
        
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_module_file_name", "Vulkan")
        self.cpp_info.set_property("cmake_file_name", "VulkanLoader")
        self.cpp_info.set_property("cmake_module_target_name", "Vulkan::Vulkan")
        self.cpp_info.set_property("cmake_target_name", "Vulkan::Loader")
