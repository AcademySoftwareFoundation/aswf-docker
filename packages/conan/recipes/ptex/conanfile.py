# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/2a3cb93885141024c1b405a01a79fb3abc239b12/recipes/ptex/all/conanfile.py

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rmdir, save
import os

from conan.tools.gnu import PkgConfigDeps

required_conan_version = ">=1.53.0"


class PtexConan(ConanFile):
    name = "ptex"
    description = "Ptex is a texture mapping system developed by Walt Disney " \
                  "Animation Studios for production-quality rendering."
    license = "BSD-3-Clause"
    topics = ("texture-mapping")
    homepage = "https://ptex.us"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch", "compiler", "build_type"
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

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")
        # ASWF: DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def requirements(self):
        self.requires("zlib/[>=1.2.11 <2]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
            destination=self.source_folder, strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["PTEX_BUILD_STATIC_LIBS"] = not self.options.shared
        tc.variables["PTEX_BUILD_SHARED_LIBS"] = self.options.shared
        tc.generate()
        cd = CMakeDeps(self)
        cd.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)
        # disable subdirs
        save(self, os.path.join(self.source_folder, "src", "utils", "CMakeLists.txt"), "")
        save(self, os.path.join(self.source_folder, "src", "tests", "CMakeLists.txt"), "")
        save(self, os.path.join(self.source_folder, "src", "doc", "CMakeLists.txt"), "")

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # ASWF: license files in package subdirs
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        # ASWF: modules in lib64
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))

    def package_info(self):
        cmake_target = "Ptex_dynamic" if self.options.shared else "Ptex_static"
        self.cpp_info.set_property("cmake_file_name", "ptex")
        self.cpp_info.set_property("cmake_target_name", f"Ptex::{cmake_target}")
        # TODO: back to global scope once cmake_find_package* generators removed
        self.cpp_info.components["_ptex"].libs = ["Ptex"]
        if not self.options.shared:
            self.cpp_info.components["_ptex"].defines.append("PTEX_STATIC")
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["_ptex"].system_libs.append("pthread")
        self.cpp_info.components["_ptex"].requires = ["zlib::zlib"]

        # TODO: to remove in conan v2 once cmake_find_package* generators removed
        self.cpp_info.filenames["cmake_find_package"] = "ptex"
        self.cpp_info.filenames["cmake_find_package_multi"] = "ptex"
        self.cpp_info.names["cmake_find_package"] = "Ptex"
        self.cpp_info.names["cmake_find_package_multi"] = "Ptex"
        self.cpp_info.components["_ptex"].set_property("cmake_target_name", f"Ptex::{cmake_target}")
        self.cpp_info.components["_ptex"].names["cmake_find_package"] = cmake_target
        self.cpp_info.components["_ptex"].names["cmake_find_package_multi"] = cmake_target
