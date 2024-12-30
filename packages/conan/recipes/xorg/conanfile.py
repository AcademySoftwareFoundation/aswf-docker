# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/4622ac85d1cec8cb7a2fcc8a1796d4b73bff285e/recipes/xorg/all/conanfile.py

from conan import ConanFile, conan_version
from conan.tools.gnu import PkgConfig
from conan.tools.system import package_manager
from conan.errors import ConanInvalidConfiguration
from conan.tools.scm import Version

required_conan_version = ">=1.50.0"


class SystemXorgConan(ConanFile):
    name = "xorg"
    version = "system"
    package_type = "shared-library"
    url = "https://github.com/conan-io/conan-center-index"
    license = "MIT"
    homepage = "https://www.x.org/wiki/"
    description = "The X.Org project provides an open source implementation of the X Window System."
    settings = "os", "arch", "compiler", "build_type"
    topics = ("x11", "xorg")

    def package_info(self):
        if Version(conan_version) >= 2:
            self.cpp_info.bindirs = []
            self.cpp_info.includedirs = []
            self.cpp_info.libdirs = []

        for name in ["x11", "x11-xcb", "fontenc", "ice", "sm", "xau", "xaw7",
                     "xcomposite", "xcursor", "xdamage", "xdmcp", "xext", "xfixes", "xi",
                     "xinerama", "xkbfile", "xmu", "xmuu", "xpm", "xrandr", "xrender", "xres",
                     "xscrnsaver", "xt", "xtst", "xv", "xxf86vm",
                     "xcb-xkb", "xcb-icccm", "xcb-image", "xcb-keysyms", "xcb-randr", "xcb-render",
                     "xcb-renderutil", "xcb-shape", "xcb-shm", "xcb-sync", "xcb-xfixes",
                     "xcb-xinerama", "xcb", "xcb-atom", "xcb-aux", "xcb-event", "xcb-util",
                     "xcb-dri3", "xcb-cursor", "xcb-dri2", "xcb-dri3", "xcb-glx", "xcb-present",
                     "xcb-composite", "xcb-ewmh", "xcb-res"] + ([] if self.settings.os == "FreeBSD" else ["uuid"]):
            pkg_config = PkgConfig(self, name)
            pkg_config.fill_cpp_info(
                self.cpp_info.components[name], is_system=self.settings.os != "FreeBSD")
            self.cpp_info.components[name].version = pkg_config.version
            self.cpp_info.components[name].set_property(
                "pkg_config_name", name)
            self.cpp_info.components[name].set_property(
                "component_version", pkg_config.version)
            self.cpp_info.components[name].bindirs = []
            self.cpp_info.components[name].includedirs = []
            self.cpp_info.components[name].libdirs = []
            self.cpp_info.components[name].set_property("pkg_config_custom_content",
                                                        "\n".join(f"{key}={value}" for key, value in pkg_config.variables.items() if key not in ["pcfiledir","prefix", "includedir"]))
