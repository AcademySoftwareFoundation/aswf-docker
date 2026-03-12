# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/pystring/all/conanfile.py

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, mkdir
import os

required_conan_version = ">=1.53.0"


class PystringConan(ConanFile):
    name = "pystring"
    description = "Pystring is a collection of C++ functions which match the " \
                  "interface and behavior of python's string class methods using std::string."
    license = "BSD-3-Clause"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/imageworks/pystring"
    topics = ("python", "string")
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

    exports_sources = "CMakeLists.txt"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["PYSTRING_SRC_DIR"] = self.source_folder.replace("\\", "/")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, os.pardir))
        cmake.build()

    def package(self):
        # ASWF: licenses in package subdirectories
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        # ASWF: a trivial CMake config to help with outside Conan builds
        cmakepath = os.path.join(self.package_folder, "lib", "cmake", "pystring")
        mkdir(self, cmakepath)
        with open(os.path.join(cmakepath, "pystringConfig.cmake"), "w") as f:
            f.write("""
if(NOT TARGET pystring::pystring)
    add_library(pystring::pystring INTERFACE IMPORTED)
endif()
""")
        with open(os.path.join(cmakepath, "pystringConfigVersion.cmake"), "w") as f:
            f.write(f"""
set(PACKAGE_VERSION "{ self.version }")
if(NOT DEFINED PACKAGE_FIND_VERSION)
    set(PACKAGE_VERSION_COMPATIBLE TRUE)
    set(PACKAGE_VERSION_EXACT TRUE)
    return()
endif()
if(PACKAGE_FIND_VERSION VERSION_LESS PACKAGE_VERSION)
    set(PACKAGE_VERSION_COMPATIBLE TRUE)
else()
    set(PACKAGE_VERSION_COMPATIBLE FALSE)
endif()
if(PACKAGE_FIND_VERSION VERSION_EQUAL PACKAGE_VERSION)
    set(PACKAGE_VERSION_EXACT TRUE)
endif()
""")

    def package_info(self):
        self.cpp_info.libs = ["pystring"]
