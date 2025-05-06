# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, collect_libs, copy, export_conandata_patches, get, rmdir
from conan.tools.microsoft import is_msvc
from conan.tools.env import Environment
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
        "shared": False,
        "fPIC": True,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")
        # ASWF: DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def requirements(self):
        self.requires(f"cpython/{os.environ['ASWF_CPYTHON_VERSION']}@{self.user}/{self.channel}")
        self.requires("zlib/[>=1.2.11 <2]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        env = Environment()
        env.define("CXXFLAGS_STD", f"c++{self.settings.get_safe('compiler.cppstd')}")
        env.vars(self).save_script("my_env")
        tc = CMakeToolchain(self)
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "partio")
        self.cpp_info.set_property("cmake_target_name", "partio::partio")
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = collect_libs(self)
        self.cpp_info.requires = ["zlib::zlib", "cpython::cpython"]
