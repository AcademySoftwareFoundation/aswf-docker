# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conans import ConanFile, tools, CMake
import os

required_conan_version = ">=1.38.0"


class OpenSubdivConan(ConanFile):
    name = "opensubdiv"
    description = "An Open-Source subdivision surface library."
    topics = "conan", "opensubdiv", "vfx"
    homepage = "https://github.com/PixarAnimationStudios/OpenSubdiv"
    license = "Apache-2.0"
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
            f"ptex/{os.environ['ASWF_PTEX_VERSION']}@{self.user}/{self.channel}"
        )
        self.requires(
            f"glfw/{os.environ['ASWF_GLFW_VERSION']}@{self.user}/{self.channel}"
        )
        self.requires(
            f"glew/{os.environ['ASWF_GLEW_VERSION']}@{self.user}/{self.channel}"
        )
        self.requires(
            f"tbb/{os.environ['ASWF_TBB_VERSION']}@{self.user}/{self.channel}"
        )

    def build_requirements(self):
        self.build_requires(
            f"cmake/{os.environ['ASWF_CMAKE_VERSION']}@{self.user}/{self.channel}"
        )

    def source(self):
        tools.get(
            f"https://github.com/PixarAnimationStudios/OpenSubdiv/archive/v{self.version}.tar.gz"
        )
        os.rename(f"OpenSubdiv-{self.version}", self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        if self.options.shared:
            del self.options.fPIC

        with tools.environment_append(tools.RunEnvironment(self).vars):
            self._cmake = CMake(self)
            if self.options.shared:
                self._cmake.definitions["BUILD_SHARED_LIBS"] = "1"
            self._cmake.definitions["NO_EXAMPLES"] = "ON"
            self._cmake.definitions["NO_REGRESSION"] = "1"
            self._cmake.definitions["NO_DOC"] = "1"
            self._cmake.definitions["NO_TUTORIAL"] = "ON"
            # Do we need to have a dynamic table here for the GPU virtual architecture?
            self._cmake.definitions[
                "OSD_CUDA_NVCC_FLAGS"
            ] = "--gpu-architecture compute_50"
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
