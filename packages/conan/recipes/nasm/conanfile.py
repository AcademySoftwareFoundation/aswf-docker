# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/b96b04ffad873992cbcfb98f0d84f6f44beb169d/recipes/nasm/all/conanfile.py

from conan import ConanFile

class SystemNASMConan(ConanFile):
    name = "nasm"
    version = "system"

    settings = "os", "arch", "compiler", "build_type"

    def package_info(self):
        self.cpp_info.includedirs = [""]
        self.cpp_info.libdirs = [""]
        self.cpp_info.bindirs = ["/usr/bin"]
        self.cpp_info.binaries = ["nasm"]

