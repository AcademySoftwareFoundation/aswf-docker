# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.files import load
import re


class SystemGnuTLSConan(ConanFile):
    name = "gnutls"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": True,
    }

    def set_version(self):
        content = load(self, "/usr/lib64/pkgconfig/gnutls.pc")
        match = re.search(r"^Version:\s*(.+)$", content, re.MULTILINE)
        self.version = match.group(1).strip()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "GnuTLS")
        self.cpp_info.set_property("pkg_config_name", "gnutls")

        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
        self.cpp_info.libs = ["gnutls"]
        self.cpp_info.system_libs = ["dl", "pthread", "z", "m"]
