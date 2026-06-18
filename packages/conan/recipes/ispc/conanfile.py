# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

import os
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get

required_conan_version = ">=2.1"


class IspcConan(ConanFile):
    name = "ispc"
    description = (
        "Intel® Implicit SPMD Program Compiler: a compiler for high-performance "
        "SIMD programming on CPUs and GPUs."
    )
    license = "BSD-3-Clause"
    url = "https://ispc.github.io/"
    homepage = "https://ispc.github.io/"
    topics = ("ispc", "compiler", "simd", "spmd")
    package_type = "application"
    settings = "os", "arch"

    def validate(self):
        if self.settings.os not in ["Linux", "Macos", "Windows"]:
            raise ConanInvalidConfiguration(f"{self.ref} is not available for {self.settings.os}")
        if self.settings.os == "Linux" and self.settings.arch not in ["x86_64", "armv8"]:
            raise ConanInvalidConfiguration(
                f"{self.ref} Linux binary is only available for x86_64 and armv8")

    def source(self):
        # source() cannot use self.settings in Conan 2.x — download in build()
        pass

    def build(self):
        arch = str(self.settings.arch)
        get(self, **self.conan_data["sources"][self.version][arch],
            strip_root=True, destination=self.build_folder)

    def package(self):
        copy(self, "LICENSE.txt",
             src=self.build_folder,
             dst=os.path.join(self.package_folder, "licenses", self.name))
        copy(self, "ispc",
             src=os.path.join(self.build_folder, "bin"),
             dst=os.path.join(self.package_folder, "bin"))
        copy(self, "*",
             src=os.path.join(self.build_folder, "include"),
             dst=os.path.join(self.package_folder, "include"))

    def package_id(self):
        # Binary-only: package id is OS + arch only (no compiler settings)
        pass

    def package_info(self):
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.libdirs = []
        self.cpp_info.includedirs = ["include"]
        # Expose the ispc executable path for downstream CMake consumers
        ispc_bin = os.path.join(self.package_folder, "bin", "ispc")
        self.conf_info.define("user.ispc:compiler", ispc_bin)
        self.buildenv_info.define_path("ISPC", ispc_bin)
