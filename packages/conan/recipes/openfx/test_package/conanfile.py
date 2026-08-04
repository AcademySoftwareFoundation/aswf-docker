# Copyright (c) Contributors to the OpenFX Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
#
# From: https://github.com/AcademySoftwareFoundation/openfx/blob/158c8b69d9a2016755696138e027fdfd71bab552/test_package/conanfile.py

import os

from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run


class openfxTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def test(self):
        if can_run(self):
            cmd = os.path.join(self.build_folder, self.cpp.build.bindir, "test_package")
            self.run(cmd, env=["conanrun"])
