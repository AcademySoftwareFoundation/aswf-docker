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


class RawtoacesConan(ConanFile):
    name = "rawtoaces"
    license = "Apache-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/AcademySoftwareFoundation/rawtoaces"
    description = "rawtoaces converts digital camera RAW files to ACES container files."
    topics = ("image", "photography", "raw")

    package_type = "application"
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
        # Conan environment overrides
        self.requires("ceres-solver/2.2.0")
        self.requires("imath/3.1.12")
        self.requires("libraw/0.21.4")
        self.requires("boost/1.88.0")
        self.requires("aces_container/1.0.2")
        # At next version the requirements below are added
        self.requires("oiio/3.0.7.0")
        self.requires("nlohmann_json/3.12.0")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["INSTALL_LIB_DIR"] = "lib64"
        tc.variables["INSTALL_CMAKE_DIR"] = os.path.join("lib64", "cmake", "RAWTOACES")
        # Dont point rpath to internal Conan directories
        tc.cache_variables["CMAKE_INSTALL_RPATH_USE_LINK_PATH"] = False
        tc.cache_variables["CMAKE_INSTALL_RPATH"] = ""
        tc.cache_variables["CMAKE_SKIP_RPATH"] = True
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
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))

    def package_info(self):
        pass

