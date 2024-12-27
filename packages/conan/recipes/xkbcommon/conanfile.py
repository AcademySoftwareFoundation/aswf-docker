# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile

class SystemXkbcommonConan(ConanFile):
    name = "xkbcommon"
    version = "0.9.1"
    
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "with_x11": [True, False],
    }
    default_options = {
        "with_x11": True,
    }

    def requirements(self):
        # self.requires("xkeyboard-config/system")
        if self.options.with_x11:
            self.requires("xorg/system")
        if self.options.get_safe("xkbregistry"):
            self.requires("libxml2/[>=2.12.5 <3]")
        if self.options.get_safe("with_wayland"):
            self.requires("wayland/1.22.0")
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]

        self.cpp_info.components["libxkbcommon"].set_property("pkg_config_name", "xkbcommon")
        self.cpp_info.components["libxkbcommon"].libs = ["xkbcommon"]
        self.cpp_info.components["libxkbcommon"].resdirs = ["res"]
        self.cpp_info.components["libxkbcommon"].includedirs = ["/usr/include"]
        
        self.cpp_info.components["libxkbcommon-x11"].set_property("pkg_config_name", "xkbcommon-x11")
        self.cpp_info.components["libxkbcommon-x11"].libs = ["xkbcommon-x11"]
        self.cpp_info.components["libxkbcommon-x11"].requires = ["libxkbcommon", "xorg::xcb", "xorg::xcb-xkb"]
        self.cpp_info.components["libxkbcommon-x11"].includedirs = ["/usr/include"]

