# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

import os

from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake, cmake_layout


class rawtoacesTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        # rawtoaces is package_type="application", so headers/libs default
        # to False for consumers unless explicitly requested -- this test
        # exercises the rawtoaces_core library, not just the CLI tool.
        self.requires(self.tested_reference_str, headers=True, libs=True)

    def build_requirements(self):
        # rawtoaces-config.cmake unconditionally emits find_dependency()
        # for every one of rawtoaces' own requires() -- including nanobind
        # -- regardless of which component we link (Conan's CMakeDeps
        # doesn't filter this by component). nanobind's own generated cmake
        # config does its own find_package(Python), and since tool_requires
        # is not transitive, this package needs cpython on PATH itself too,
        # or that Python detection finds nothing usable. Mirrors rawtoaces'
        # own build_requirements().
        self.tool_requires("cpython/[>=3.0.0]")

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
