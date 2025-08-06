# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/feef5a8b9d03692bf27a8e1e94a6f59fd493d420/recipes/opencl-icd-loader/all/conanfile.py

from conan import ConanFile

class SystemOpenclIcdLoaderConan(ConanFile):
    name = "opencl-icd-loader"
    version = "system"

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.system_libs = ["OpenCL"]
       
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_module_file_name", "OpenCL")
        self.cpp_info.set_property("cmake_file_name", "OpenCLICDLoader")
        self.cpp_info.set_property("cmake_target_name", "OpenCL::OpenCL")
