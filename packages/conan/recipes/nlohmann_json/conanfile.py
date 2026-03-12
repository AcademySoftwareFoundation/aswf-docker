# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5f19361f49bc31a349b383c1f95c7f79627f728a/recipes/nlohmann_json/all/conanfile.py

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy, get, mkdir
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=1.50.0"


class NlohmannJsonConan(ConanFile):
    name = "nlohmann_json"
    homepage = "https://github.com/nlohmann/json"
    description = "JSON for Modern C++ parser and generator."
    topics = "json", "header-only"
    url = "https://github.com/conan-io/conan-center-index"
    license = "MIT"
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    @property
    def _minimum_cpp_standard(self):
        return 11

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, self._minimum_cpp_standard)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        pass

    def build(self):
        pass

    def package(self):
        # ASWF: license file in package specific directories
        copy(self, "LICENSE*", self.source_folder, os.path.join(self.package_folder, "licenses", self.name))
        copy(self, "*", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        # ASWF: a trivial CMake config to help with outside Conan builds
        cmakepath = os.path.join(self.package_folder, "lib", "cmake", "nlohmann_json")
        mkdir(self, cmakepath)
        with open(os.path.join(cmakepath, "nlohmann_jsonConfig.cmake"), "w") as f:
            f.write("""
if(NOT TARGET nlohmann_json::nlohmann_json)
    add_library(nlohmann_json::nlohmann_json INTERFACE IMPORTED)
endif()
""")
        with open(os.path.join(cmakepath, "nlohmann_jsonConfigVersion.cmake"), "w") as f:
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
        self.cpp_info.set_property("cmake_file_name", "nlohmann_json")
        self.cpp_info.set_property("cmake_target_name", "nlohmann_json::nlohmann_json")
        self.cpp_info.set_property("pkg_config_name", "nlohmann_json")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
