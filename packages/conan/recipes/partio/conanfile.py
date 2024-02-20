# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conans import ConanFile, tools, CMake
import os

required_conan_version = ">=1.38.0"


class PartioConan(ConanFile):
    name = "partio"
    description = "C++ (with python bindings) library for easily reading/writing/manipulating common animation particle formats such as PDB, BGEO, PTC."
    topics = "conan", "partio", "vfx"
    homepage = "https://github.com/wdas/partio"
    license = "BSD-3-Clause"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    settings = (
        "os",
        "arch",
        "compiler",
        "build_type",
    )
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
    }
    generators = "cmake_find_package_multi"

    _cmake = None
    _source_subfolder = "source_subfolder"

    def requirements(self):
        self.requires(
            f"python/{os.environ['ASWF_PYTHON_VERSION']}@{self.user}/{self.channel}"
        )

    def build_requirements(self):
        self.build_requires(
            f"cmake/{os.environ['ASWF_CMAKE_VERSION']}@{self.user}/{self.channel}"
        )

    def source(self):
        tools.get(f"https://github.com/wdas/partio/archive/v{self.version}.tar.gz")
        os.rename(f"partio-{self.version}", self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        if self.options.shared:
            del self.options.fPIC

        with tools.environment_append(tools.RunEnvironment(self).vars):
            self._cmake = CMake(self)
            self._cmake.configure(source_folder=self._source_subfolder)
            return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build(args=["--verbose"])

    def package(self):
        self.copy("LICENSE.md", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.env_info.CMAKE_PREFIX_PATH.append(
            os.path.join(self.package_folder, "lib", "cmake")
        )

    def deploy(self):
        self.copy("*")
