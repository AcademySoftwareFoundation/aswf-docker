# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/opus/all/conanfile.py

from conan import ConanFile

class SystemOpusConan(ConanFile):
    name = "opus"
    version = "wrapper"
    
    settings = "os", "arch", "compiler", "build_type"

    def package_info(self):
        self.cpp_info.libdirs = ["/usr/lib64"]

        self.cpp_info.set_property("cmake_file_name", "Opus")
        self.cpp_info.set_property("cmake_target_name", "Opus::opus")
        self.cpp_info.set_property("pkg_config_name", "opus")
        self.cpp_info.libs = ["opus"]
        self.cpp_info.includedirs.append("/usr/include/opus")
        self.cpp_info.system_libs.append("m")
