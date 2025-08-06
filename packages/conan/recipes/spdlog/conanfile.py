# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/feef5a8b9d03692bf27a8e1e94a6f59fd493d420/recipes/spdlog/all/conanfile.py

from conan import ConanFile

class SystemSpdlogConan(ConanFile):
    name = "spdlog"
    version = "system"

    def requirements(self):
      # Conan profile provides real versions
      self.requires("fmt/[>=11.0.0]", transitive_headers=True, transitive_libs=True)

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.system_libs = ["spdlog"]
       
        self.cpp_info.set_property("cmake_file_name", "spdlog")
        self.cpp_info.set_property("cmake_target_name", "spdlog::spdlog") 

        self.cpp_info.components["libspdlog"].set_property("cmake_target_name", "spdlog::spdlog")
        self.cpp_info.components["libspdlog"].requires = ["fmt::fmt"]
        self.cpp_info.components["libspdlog"].defines.append("SPDLOG_FMT_EXTERNAL")
