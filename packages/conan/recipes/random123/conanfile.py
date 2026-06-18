# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.files import get, copy
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=1.50.0"


class Random123Conan(ConanFile):
    name = "random123"
    description = (
        "A library of counter-based random number generators (CBRNGs) for "
        "CPUs (C and C++) and GPUs (CUDA and OpenCL)."
    )
    topics = ("random", "rng", "counter-based", "header-only")
    url = "https://github.com/DEShawResearch/random123"
    homepage = "https://github.com/DEShawResearch/random123"
    license = "BSD-3-Clause"
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def layout(self):
        basic_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package(self):
        copy(self, pattern="LICENSE",
             src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses", self.name))
        copy(self, pattern="*",
             src=os.path.join(self.source_folder, "include"),
             dst=os.path.join(self.package_folder, "include"))

    def package_id(self):
        self.info.clear()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Random123")
        self.cpp_info.set_property("cmake_target_name", "Random123::Random123")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
