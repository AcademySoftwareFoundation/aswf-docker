# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.files import load
import re

class SystemXkbcommonConan(ConanFile):
    name = "xkbcommon"
    
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "with_x11": [True, False],
    }
    default_options = {
        "with_x11": True,
    }

    def set_version(self):
        content = load(self, "/usr/lib64/pkgconfig/xkbcommon.pc")
        match = re.search(r"^Version:\s*(.+)$", content, re.MULTILINE)
        self.version = match.group(1).strip()

    def requirements(self):
        # self.requires("xkeyboard-config/system")
        if self.options.with_x11:
            self.requires("xorg/system")
        if self.options.get_safe("xkbregistry"):
            self.requires("libxml2/[>=2.12.5 <3]")
        if self.options.get_safe("with_wayland"):
            self.requires("wayland/1.22.0")
   
    def package_info(self):
        self.cpp_info.includedirs = []

        self.cpp_info.components["libxkbcommon"].set_property("pkg_config_name", "xkbcommon")
        self.cpp_info.components["libxkbcommon"].system_libs = ["xkbcommon"]
        self.cpp_info.components["libxkbcommon"].resdirs = ["res"]
        self.cpp_info.components["libxkbcommon"].includedirs = []
        
        self.cpp_info.components["libxkbcommon-x11"].set_property("pkg_config_name", "xkbcommon-x11")
        self.cpp_info.components["libxkbcommon-x11"].system_libs = ["xkbcommon-x11"]
        self.cpp_info.components["libxkbcommon-x11"].requires = ["libxkbcommon", "xorg::xcb", "xorg::xcb-xkb"]
        self.cpp_info.components["libxkbcommon-x11"].includedirs = []

