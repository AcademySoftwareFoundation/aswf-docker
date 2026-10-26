# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.files import load
import re

class SystemLibdrmConan(ConanFile):
    name = "libdrm"

    settings = "os", "arch", "compiler", "build_type"

    def set_version(self):
        # Advertise the real, system-installed version instead of the
        # literal string "system", so consumers that version-check this
        # dependency via pkg-config (e.g. mesa's meson.build requiring
        # libdrm >=2.4.109) see a real, comparable version instead of
        # failing with "Invalid version ... found 'system'".
        content = load(self, "/usr/lib64/pkgconfig/libdrm.pc")
        match = re.search(r"^Version:\s*(.+)$", content, re.MULTILINE)
        self.version = match.group(1).strip()

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
