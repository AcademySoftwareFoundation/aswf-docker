# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/3c237f4a7e8f29eacae90b809e4f18e75dfc05a3/recipes/rapidjson/all/conanfile.py

from conan import ConanFile
from conan.tools.files import get, copy, mkdir
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=1.50.0"


class RapidjsonConan(ConanFile):
    name = "rapidjson"
    description = "A fast JSON parser/generator for C++ with both SAX/DOM style API"
    topics = ("rapidjson", "json", "parser", "generator")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://rapidjson.org"
    license = "MIT"
    package_type = "header-library"
    package_id_embed_mode = "minor_mode"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def layout(self):
        basic_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True,
                    destination=self.source_folder)

    def package(self):
        copy(self, pattern="license.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name)) # ASWF: licenses in package dir
        copy(self, pattern="*", src=os.path.join(self.source_folder, "include"), dst=os.path.join(self.package_folder, "include"))
        # ASWF: a trivial CMake config to help with outside Conan builds
        cmakepath = os.path.join(self.package_folder, "lib", "cmake", "RapidJSON")
        mkdir(self, cmakepath)
        with open(os.path.join(cmakepath, "RapidJSONConfig.cmake"), "w") as f:
            f.write("""
if(NOT TARGET RapidJSON::RapidJSON)
    add_library(RapidJSON::RapidJSON INTERFACE IMPORTED)
endif()
""")
        with open(os.path.join(cmakepath, "RapidJSONConfigVersion.cmake"), "w") as f:
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

    def package_id(self):
        self.info.clear()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "RapidJSON")
        self.cpp_info.set_property("cmake_target_name", "rapidjson")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

        # TODO: to remove in conan v2 once cmake_find_package* generators removed
        self.cpp_info.names["cmake_find_package"] = "RapidJSON"
        self.cpp_info.names["cmake_find_package_multi"] = "RapidJSON"
