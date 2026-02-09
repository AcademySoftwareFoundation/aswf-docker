# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.files import load
import re


class SystemOpenSSLConan(ConanFile):
    name = "openssl"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": True,
    }

    def set_version(self):
        content = load(self, "/usr/lib64/pkgconfig/openssl.pc")
        match = re.search(r"^Version:\s*(.+)$", content, re.MULTILINE)
        self.version = match.group(1).strip()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "OpenSSL")
        self.cpp_info.set_property("pkg_config_name", "openssl")

        # Point to system OpenSSL
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]

        # Component: Crypto
        self.cpp_info.components["Crypto"].set_property("cmake_target_name", "OpenSSL::Crypto")
        self.cpp_info.components["Crypto"].libs = ["crypto"]
        self.cpp_info.components["Crypto"].includedirs = ["/usr/include"]
        self.cpp_info.components["Crypto"].libdirs = ["/usr/lib64"]
        self.cpp_info.components["Crypto"].system_libs = ["dl", "pthread"]

        # Component: SSL
        self.cpp_info.components["SSL"].set_property("cmake_target_name", "OpenSSL::SSL")
        self.cpp_info.components["SSL"].libs = ["ssl"]
        self.cpp_info.components["SSL"].includedirs = ["/usr/include"]
        self.cpp_info.components["SSL"].libdirs = ["/usr/lib64"]
        self.cpp_info.components["SSL"].requires = ["Crypto"]
