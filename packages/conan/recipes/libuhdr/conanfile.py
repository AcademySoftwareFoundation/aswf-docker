# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rmdir
import glob
import os

required_conan_version = ">=2.0"

class LibuhdrConan(ConanFile):
    name = "libuhdr"
    license = "Apache-2.0"
    url = "https://github.com/google/libultrahdr"
    homepage = "https://github.com/google/libultrahdr"
    description = "libuhdr is an image compression library that uses gain map technology to store and distribute HDR images."
    topics = ("hdr", "image compression", "gain map", "high dynamic range")

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
      "shared": False,
      "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)
        # ASWF: we want DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        # Copy license file if it is not copied by CMake install
        copy(self, "LICENSE", dst=os.path.join(self.package_folder, "licenses", self.name), src=self.source_folder, keep_path=False)
        # Keep cmake files for non-Conan clients
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))

        # Clean up static lib if building dynamic
        if self.options.shared:
            for lib in glob.glob(os.path.join(self.package_folder, "lib64", "*.a")):
                if not lib.endswith(".dll.a"):
                    os.remove(lib)

    def package_info(self):
        self.cpp_info.libs = ["uhdr"]
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "LIBUHDR")
        self.cpp_info.set_property("cmake_target_name", "LIBUHDR::LIBUHDR")
