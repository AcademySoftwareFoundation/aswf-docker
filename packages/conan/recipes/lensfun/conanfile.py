# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, collect_libs, copy, export_conandata_patches, get, rmdir
import os

required_conan_version = ">=2.0"


class LensfunConan(ConanFile):
    name = "lensfun"
    description = "Open source lens database and image correction library."
    license = "LGPL-3.0-only"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    homepage = "https://github.com/lensfun/lensfun"
    topics = ("image", "photography", "lens", "database")
    package_type = "library"
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

    def requirements(self):
        self.requires("glib/2.56.4")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        apply_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["BUILD_STATIC"] = not self.options.shared
        tc.cache_variables["BUILD_TESTS"] = False
        tc.cache_variables["BUILD_LENSTOOL"] = False
        tc.cache_variables["BUILD_DOC"] = False
        tc.cache_variables["INSTALL_PYTHON_MODULE"] = False
        tc.cache_variables["INSTALL_HELPER_SCRIPTS"] = False
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "COPYING.LESSER", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        # rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig")) # ASWF: rawtoaces uses pkgconfig to find lensfun

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "lensfun")
        self.cpp_info.set_property("cmake_target_name", "lensfun::lensfun")
        self.cpp_info.set_property("pkg_config_name", "lensfun")
        self.cpp_info.libs = collect_libs(self)
