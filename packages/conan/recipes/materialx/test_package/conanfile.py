# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import cmake_layout, CMake
from conans import tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type", "python"
    generators = "CMakeDeps", "CMakeToolchain", "VirtualRunEnv"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        with tools.environment_append(tools.RunEnvironment(self).vars):
            cmake.configure()
            cmake.build()

    def test(self):
        if can_run(self):
            bin_path = os.path.join(self.cpp.build.bindir, "test_package")
            self.run(bin_path, env="conanrun")
        self.run(
            "{} {}".format(
                self.deps_user_info["python"].python_interp,
                os.path.join(self.source_folder, "test_package.py"),
            ),
            run_environment=True,
        )
