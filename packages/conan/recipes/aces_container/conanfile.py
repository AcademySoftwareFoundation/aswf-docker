# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">=2"


class ACESContainerConan(ConanFile):
    name = "aces_container"
    license = "AMPAS ACES Container"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://acescentral.com/"
    description = "Reference Implementation of SMPTE ST2065-4."
    topics = ("aces", "image", "picture")

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
        # ASWF: DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["INSTALL_LIB_DIR"] = "lib64"
        tc.variables["INSTALL_CMAKE_DIR"] = os.path.join("lib64", "cmake", "AcesContainer")
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # ASWF: separate license files per package
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        # aces_container CMakeLists.txt hard codes lib/pkgconfig
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "AcesContainer")
        self.cpp_info.set_property("cmake_target_name", "AcesContainer::AcesContainer")
        self.cpp_info.libs = ["AcesContainer"]
