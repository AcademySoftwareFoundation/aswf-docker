# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/libdrm/all/conanfile.py

from conan import ConanFile

class SystemLibdrmConan(ConanFile):
    name = "libdrm"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"

    def package_info(self):
        self.cpp_info.system_libs = ["drm", "drm_amdgpu", "drm_nouveau", "drm_intel", "drm_radeon"]
        self.cpp_info.includedirs = ["/usr/include/libdrm", "/usr/include/libdrm/nouveau"]

        self.cpp_info.set_property("cmake_file_name", "Libdrm")
        self.cpp_info.set_property("cmake_target_name", "Libdrm::Libdrm")

        # self.cpp_info.components["libdrm_libdrm"].libs = ["drm"]
        # self.cpp_info.components["libdrm_libdrm"].includedirs.append("/usr/include/libdrm")
        # self.cpp_info.components["libdrm_libdrm"].set_property("pkg_config_name", "libdrm")

        # self.cpp_info.components["libdrm_amdgpu"].libs = ["drm_amdgpu"]
        # self.cpp_info.components["libdrm_amdgpu"].includedirs.append("/usr/include/libdrm")
        # self.cpp_info.components["libdrm_amdgpu"].requires = ["libdrm_libdrm"]
        # self.cpp_info.components["libdrm_amdgpu"].set_property("pkg_config_name", "libdrm_amdgpu")

        # self.cpp_info.components["libdrm_nouveau"].libs = ["drm_nouveau"]
        # self.cpp_info.components["libdrm_nouveau"].includedirs.extend(["/usr/include/libdrm", "/usr/include/libdrm/nouveau"])
        # self.cpp_info.components["libdrm_nouveau"].requires = ["libdrm_libdrm"]
        # self.cpp_info.components["libdrm_nouveau"].system_libs = ["pthread"]
        # self.cpp_info.components["libdrm_nouveau"].set_property("pkg_config_name", "libdrm_nouveau")

        # self.cpp_info.components["libdrm_intel"].libs = ["drm_intel"]
        # self.cpp_info.components["libdrm_intel"].includedirs.append("/usr/include/libdrm")
        # self.cpp_info.components["libdrm_intel"].requires = ["libdrm_libdrm"]
        # self.cpp_info.components["libdrm_intel"].set_property("pkg_config_name", "libdrm_intel")

        # self.cpp_info.components["libdrm_radeon"].libs = ["drm_radeon"]
        # self.cpp_info.components["libdrm_radeon"].includedirs.append("/usr/include/libdrm")
        # self.cpp_info.components["libdrm_radeon"].requires = ["libdrm_libdrm"]
        # self.cpp_info.components["libdrm_radeon"].set_property("pkg_config_name", "libdrm_radeon")
