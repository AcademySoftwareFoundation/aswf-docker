# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rmdir
import os

required_conan_version = ">=1.53.0"


class JsoncppConan(ConanFile):
    name = "jsoncpp"
    description = "A C++ library for interacting with JSON."
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/open-source-parsers/jsoncpp"
    topics = ("json", "parser", "config")
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
        tc.variables["JSONCPP_WITH_TESTS"] = False
        tc.variables["JSONCPP_WITH_POST_BUILD_UNITTEST"] = False
        tc.variables["JSONCPP_WITH_WARNING_AS_ERROR"] = False
        tc.variables["JSONCPP_WITH_PKGCONFIG_SUPPORT"] = False
        tc.variables["JSONCPP_WITH_CMAKE_PACKAGE"] = True
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["BUILD_STATIC_LIBS"] = not self.options.shared
        tc.variables["BUILD_OBJECT_LIBS"] = False
        # Disable ccache detection
        tc.cache_variables["CCACHE_EXECUTABLE"] = ""
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # ASWF: separate licenses from multiple package installs
        copy(self, "LICENSE", src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        # ASWF: keep cmake files, delete pkgconfig files
        #rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "jsoncpp")
        self.cpp_info.set_property("cmake_target_name", "JsonCpp::JsonCpp")
        self.cpp_info.set_property("pkg_config_name", "jsoncpp")
        self.cpp_info.libs = ["jsoncpp"]
        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.defines.append("JSON_DLL")
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("m")
