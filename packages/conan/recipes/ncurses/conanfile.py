# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/ncurses/all/conanfile.py

import os

from conan import ConanFile

class SystemNCursesConan(ConanFile):
    name = "ncurses"
    version = "wrapper"
    
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_widec": [True, False],
        "with_extended_colors": [True, False],
        "with_cxx": [True, False],
        "with_progs": [True, False],
        "with_ticlib": ["auto", True, False],
        "with_reentrant": [True, False],
        "with_tinfo": ["auto", True, False],
        "with_pcre2": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_widec": True,
        "with_extended_colors": True,
        "with_cxx": False,
        "with_progs": True,
        "with_ticlib": False,
        "with_reentrant": False,
        "with_tinfo": False,
        "with_pcre2": False,
    }
   
    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "Curses")
        self.cpp_info.set_property("cmake_target_name", "Curses::Curses")

        def _add_component(name, lib_name=None, requires=None):
            lib_name = lib_name or name
            self.cpp_info.components[name].libs = [lib_name + "w"]
            self.cpp_info.components[name].set_property("pkg_config_name", lib_name + "w")
            self.cpp_info.components[name].includedirs.append(os.path.join("include", "ncurses" + "w"))
            self.cpp_info.components[name].requires = requires if requires else []

        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
 
        _add_component("libcurses", lib_name="ncurses")
        _add_component("panel", requires=["libcurses"])
        _add_component("menu", requires=["libcurses"])
        _add_component("form", requires=["libcurses"])

