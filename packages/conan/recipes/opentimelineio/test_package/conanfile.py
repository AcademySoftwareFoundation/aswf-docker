# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#

from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.scm import Version
import os


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps", "VirtualRunEnv"
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        # Headers before 0.16 / some 0.17.x installs do not expose numeric version
        # macros; Conan package version is authoritative for clip_if vs find_clips.
        if Version(self.dependencies["opentimelineio"].ref.version) < "0.16":
            tc.preprocessor_definitions["OTIO_USE_CLIP_IF"] = "1"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            bin_path = os.path.join(self.cpp.build.bindir, "test_package")
            otio_path = os.path.join(self.source_folder, "taco.otio")
            self.run(f"{bin_path} {otio_path}", env="conanrun")
