# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/icu/all/conanfile.py

from conan import ConanFile

class SystemICUConan(ConanFile):
    name = "icu"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
   
    def package_info(self):
        self.cpp_info.includedirs = []
        
        self.cpp_info.set_property("cmake_file_name", "ICU")
        self.cpp_info.set_property("cmake_target_name", "ICU::ICU")

        # icudata
        self.cpp_info.components["icu-data"].set_property("cmake_target_name", "ICU::data")
        self.cpp_info.components["icu-data"].libs = ["icudata"]

        # Alias of data CMake component
        self.cpp_info.components["icu-data-alias"].set_property("cmake_target_name", "ICU::dt")
        self.cpp_info.components["icu-data-alias"].requires = ["icu-data"]

        # icuuc
        self.cpp_info.components["icu-uc"].set_property("cmake_target_name", "ICU::uc")
        self.cpp_info.components["icu-uc"].system_libs = ["icuuc", "m", "pthread"]
        self.cpp_info.components["icu-uc"].requires = ["icu-data"]

        # icui18n
        self.cpp_info.components["icu-i18n"].set_property("cmake_target_name", "ICU::i18n")
        self.cpp_info.components["icu-i18n"].systemlibs = ["icui18n", "m"]
        self.cpp_info.components["icu-i18n"].requires = ["icu-uc"]

        # Alias of i18n CMake component
        self.cpp_info.components["icu-i18n-alias"].set_property("cmake_target_name", "ICU::in")
        self.cpp_info.components["icu-i18n-alias"].requires = ["icu-i18n"]

        # icuio
        self.cpp_info.components["icu-io"].set_property("cmake_target_name", "ICU::io")
        self.cpp_info.components["icu-io"].system_libs = ["icuio"]
        self.cpp_info.components["icu-io"].requires = ["icu-i18n", "icu-uc"]

        # icutu
        self.cpp_info.components["icu-tu"].set_property("cmake_target_name", "ICU::tu")
        self.cpp_info.components["icu-tu"].system_libs = ["icutu", "pthread"]
        self.cpp_info.components["icu-tu"].requires = ["icu-i18n", "icu-uc"]

        # icutest
        self.cpp_info.components["icu-test"].set_property("cmake_target_name", "ICU::test")
        self.cpp_info.components["icu-test"].system_libs = ["icutest"]
        self.cpp_info.components["icu-test"].requires = ["icu-tu", "icu-uc"]
