# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/glib/all/conanfile.py

from conan import ConanFile
from conan.tools.files import load
import os
import re

class SystemGLibConan(ConanFile):
    name = "glib"
    settings = "os", "arch", "compiler", "build_type"

    def set_version(self):
        content = load(self, "/usr/lib64/pkgconfig/glib-2.0.pc")
        match = re.search(r"^Version:\s*(.+)$", content, re.MULTILINE)
        self.version = match.group(1).strip()

    def requirements(self):
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires("libffi/3.4.4")
        self.requires("pcre2/10.42")
   
    def package_info(self):
        self.cpp_info.components["glib-2.0"].set_property("pkg_config_name", "glib-2.0")
        self.cpp_info.components["glib-2.0"].system_libs = ["glib-2.0"]
        self.cpp_info.components["glib-2.0"].includedirs += [
            os.path.join("include", "glib-2.0"),
            os.path.join("lib", "glib-2.0", "include")
        ]
        self.cpp_info.components["glib-2.0"].resdirs = ["res"]

        self.cpp_info.components["gmodule-no-export-2.0"].set_property("pkg_config_name", "gmodule-no-export-2.0")
        self.cpp_info.components["gmodule-no-export-2.0"].system_libs = ["gmodule-2.0"]
        self.cpp_info.components["gmodule-no-export-2.0"].resdirs = ["res"]
        self.cpp_info.components["gmodule-no-export-2.0"].requires.append("glib-2.0")

        self.cpp_info.components["gmodule-export-2.0"].set_property("pkg_config_name", "gmodule-export-2.0")
        self.cpp_info.components["gmodule-export-2.0"].requires += ["gmodule-no-export-2.0", "glib-2.0"]

        self.cpp_info.components["gmodule-2.0"].set_property("pkg_config_name", "gmodule-2.0")
        self.cpp_info.components["gmodule-2.0"].requires += ["gmodule-no-export-2.0", "glib-2.0"]

        self.cpp_info.components["gobject-2.0"].set_property("pkg_config_name", "gobject-2.0")
        self.cpp_info.components["gobject-2.0"].system_libs = ["gobject-2.0"]
        self.cpp_info.components["gobject-2.0"].resdirs = ["res"]
        self.cpp_info.components["gobject-2.0"].requires += ["glib-2.0", "libffi::libffi"]

        self.cpp_info.components["gthread-2.0"].set_property("pkg_config_name", "gthread-2.0")
        self.cpp_info.components["gthread-2.0"].system_libs = ["gthread-2.0"]
        self.cpp_info.components["gthread-2.0"].resdirs = ["res"]
        self.cpp_info.components["gthread-2.0"].requires.append("glib-2.0")

        self.cpp_info.components["gio-2.0"].set_property("pkg_config_name", "gio-2.0")
        self.cpp_info.components["gio-2.0"].system_libs = ["gio-2.0"]
        self.cpp_info.components["gio-2.0"].resdirs = ["res"]
        self.cpp_info.components["gio-2.0"].requires += ["glib-2.0", "gobject-2.0", "gmodule-2.0", "zlib::zlib"]

        self.cpp_info.components["gresource"].set_property("pkg_config_name", "gresource")
        self.cpp_info.components["gresource"].system_libs = []  # this is actually an executable

        self.cpp_info.components["glib-2.0"].system_libs.append("pthread")
        self.cpp_info.components["gmodule-no-export-2.0"].system_libs.append("pthread")
        self.cpp_info.components["gmodule-no-export-2.0"].system_libs.append("dl")
        self.cpp_info.components["gmodule-export-2.0"].sharedlinkflags.append("-Wl,--export-dynamic")
        self.cpp_info.components["gmodule-2.0"].sharedlinkflags.append("-Wl,--export-dynamic")
        self.cpp_info.components["gthread-2.0"].system_libs.append("pthread")
        self.cpp_info.components["gio-2.0"].system_libs.append("dl")

        self.cpp_info.components["gio-unix-2.0"].set_property("pkg_config_name", "gio-unix-2.0")
        self.cpp_info.components["gio-unix-2.0"].requires += ["gobject-2.0", "gio-2.0"]
        self.cpp_info.components["gio-unix-2.0"].includedirs = [os.path.join("include", "gio-unix-2.0")]

        self.cpp_info.components["glib-2.0"].requires.append("pcre2::pcre2")

        self.cpp_info.components["gio-2.0"].system_libs.append("resolv")

        # if self.options.get_safe("with_mount"):
        #     self.cpp_info.components["gio-2.0"].requires.append("libmount::libmount")

        # if self.options.get_safe("with_selinux"):
        #     self.cpp_info.components["gio-2.0"].requires.append("libselinux::libselinux")

        # if self.options.get_safe("with_elf"):
        #     self.cpp_info.components["gresource"].requires.append("libelf::libelf")  # this is actually an executable

        self.env_info.GLIB_COMPILE_SCHEMAS = os.path.join(self.package_folder, "bin", "glib-compile-schemas")
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))

        pkgconfig_variables = {
            'datadir': '${prefix}/res',
            'schemasdir': '${datadir}/glib-2.0/schemas',
            'bindir': '${prefix}/bin',
            # Can't use libdir here as it is libdir1 when using the PkgConfigDeps generator.
            'giomoduledir': '${prefix}/lib/gio/modules',
            'gio': '${bindir}/gio',
            'gio_querymodules': '${bindir}/gio-querymodules',
            'glib_compile_schemas': '${bindir}/glib-compile-schemas',
            'glib_compile_resources': '${bindir}/glib-compile-resources',
            'gdbus': '${bindir}/gdbus',
            'gdbus_codegen': '${bindir}/gdbus-codegen',
            'gresource': '${bindir}/gresource',
            'gsettings': '${bindir}/gsettings'
        }
        self.cpp_info.components["gio-2.0"].set_property(
            "pkg_config_custom_content",
            "\n".join(f"{key}={value}" for key,value in pkgconfig_variables.items()))

        pkgconfig_variables = {
            'bindir': '${prefix}/bin',
            'glib_genmarshal': '${bindir}/glib-genmarshal',
            'gobject_query': '${bindir}/gobject-query',
            'glib_mkenums': '${bindir}/glib-mkenums'
        }
        self.cpp_info.components["glib-2.0"].set_property(
            "pkg_config_custom_content",
            "\n".join(f"{key}={value}" for key, value in pkgconfig_variables.items()))

