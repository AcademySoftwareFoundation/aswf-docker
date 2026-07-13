# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

import os
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rmdir
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv

required_conan_version = ">=2.1"

class OpenImageDenoiseConan(ConanFile):
    name = "openimagedenoise"
    package_type = "shared-library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared":    [True, False],
        "fPIC":      [True, False],
        "with_cuda": [True, False],
        "with_sycl": [True, False],
        "with_hip":  [True, False],
    }
    default_options = {
        "shared":    True,
        "fPIC":      True,
        "with_cuda": True,   # ASWF: CI containers have CUDA system install
        "with_sycl": False,
        "with_hip":  False,
    }
    implements = ["auto_shared_fpic"]

    def export_sources(self):
        export_conandata_patches(self)

    def validate(self):
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration("Linux only")
        if self.settings.arch != "x86_64":
            raise ConanInvalidConfiguration("x86_64 only")

    def requirements(self):
        self.requires("onetbb/2023.0.0")  # version redirected by profile per year

    def build_requirements(self):
        clang_ref = self.conf.get("user.aswf:openimagedenoise_clang_ref", check_type=str)
        # Tool dep: llvm-config, clang, clang++ … on PATH during cmake configure/build.
        self.tool_requires(clang_ref)
        # ispc compiles CPU SIMD kernels; version redirected by profile's
        # [replace_tool_requires] (e.g. ispc/1.24.0 for vfx2024).
        self.tool_requires("ispc/1.21.0")
        self.tool_requires("cmake/[>=3.15 <4]")
        self.tool_requires("ninja/[>=1.0.0]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        VirtualBuildEnv(self).generate()  # puts ispc on PATH for cmake find_program()
        tc = CMakeToolchain(self, generator="Ninja")
        tc.variables["OIDN_APPS"] = False
        tc.variables["OIDN_INSTALL_DEPENDENCIES"] = False
        tc.variables["OIDN_DEVICE_CPU"]  = True
        tc.variables["OIDN_DEVICE_CUDA"] = self.options.with_cuda
        tc.variables["OIDN_DEVICE_SYCL"] = self.options.with_sycl
        tc.variables["OIDN_DEVICE_HIP"]  = self.options.with_hip
        tc.generate()
        CMakeDeps(self).generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE.txt", src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        # ASWF: keep cmake config files; moonray and other consumers use them
        # rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenImageDenoise")
        self.cpp_info.set_property("cmake_target_name", "OpenImageDenoise")
        self.cpp_info.libs = ["OpenImageDenoise"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.bindirs = ["bin"]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread", "dl", "m"]