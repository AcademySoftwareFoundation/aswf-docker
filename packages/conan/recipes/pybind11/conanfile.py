# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/b8bd958a29ef769d74a40471f1ada0426d1f8fff/recipes/pybind11/all/conanfile.py

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools.layout import basic_layout
from conan.tools.files import get, copy, rename, replace_in_file, rm, rmdir
from conan.tools.scm import Version
import os


required_conan_version = ">=1.52.0"


class PyBind11Conan(ConanFile):
    name = "pybind11"
    description = "Seamless operability between C++11 and Python"
    license = "BSD-3-Clause"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/pybind/pybind11"
    topics = ("pybind11", "python", "binding", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def requirements(self):
        self.requires(f"cpython/{os.environ['ASWF_CPYTHON_VERSION']}@{self.user}/{self.channel}")

    def layout(self):
        basic_layout(self, src_folder="src")
        # ASWF: We want DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def package_id(self):
        self.info.clear()

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["PYBIND11_INSTALL"] = True
        tc.variables["PYBIND11_TEST"] = False
        # ASWF: Cmake modules in lib64
        tc.variables["PYBIND11_CMAKECONFIG_INSTALL_DIR"] = os.path.join("lib64", "cmake", "pybind11")
        tc.variables["PYBIND11_PYTHON_VERSION"] = os.environ["ASWF_CPYTHON_VERSION"]
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # ASWF: prevent license files from overwritting each other when installing multiple packages
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        # ASWF: don't remove cmake files for standalone cmake use
        # for filename in ["pybind11Targets.cmake", "pybind11Config.cmake", "pybind11ConfigVersion.cmake"]:
        #  rm(self, filename, os.path.join(self.package_folder, "lib64", "cmake", "pybind11"))

        rmdir(self, os.path.join(self.package_folder, "share"))

        # ASWF: stash unmodified copy of pybind11Common.cmake for builds outside Conan
        rename(self, src=os.path.join(self.package_folder, "lib64", "cmake", "pybind11", "pybind11Common.cmake"),
               dst=os.path.join(self.package_folder, "lib64", "cmake", "pybind11", "pybind11Common.cmake_NO_CONAN"))
        copy(self, "pybind11Common.cmake", src=os.path.join(self.source_folder, "tools"),
             dst=os.path.join(self.package_folder, "lib64", "cmake", "pybind11"), overwrite_equal = True, keep_path=False)
      
        checked_target = "lto" if self.version < Version("2.11.0") else "pybind11"
        # ASWF: CMake modules in lib64/cmake
        replace_in_file(self, os.path.join(self.package_folder, "lib64", "cmake", "pybind11", "pybind11Common.cmake"),
                              f"if(TARGET pybind11::{checked_target})",
                              "if(FALSE)")
        replace_in_file(self, os.path.join(self.package_folder, "lib64", "cmake", "pybind11", "pybind11Common.cmake"),
                              "add_library(",
                              "# add_library(")

    def package_info(self):
        # ASWF: CMake modules in lib64/cmake
        cmake_base_path = os.path.join("lib64", "cmake", "pybind11")
        self.cpp_info.set_property("cmake_target_name", "pybind11_all_do_not_use")
        self.cpp_info.components["headers"].includedirs = ["include"]
        self.cpp_info.components["pybind11_"].set_property("cmake_target_name", "pybind11::pybind11")
        self.cpp_info.components["pybind11_"].set_property("cmake_module_file_name", "pybind11")
        self.cpp_info.components["pybind11_"].builddirs = [cmake_base_path]
        self.cpp_info.components["pybind11_"].requires = ["headers"]
        cmake_file = os.path.join(cmake_base_path, "pybind11Common.cmake")
        self.cpp_info.set_property("cmake_build_modules", [cmake_file])
        self.cpp_info.components["embed"].requires = ["pybind11_"]
        self.cpp_info.components["module"].requires = ["pybind11_"]
        self.cpp_info.components["python_link_helper"].requires = ["pybind11_"]
        self.cpp_info.components["windows_extras"].requires = ["pybind11_"]
        self.cpp_info.components["lto"].requires = ["pybind11_"]
        self.cpp_info.components["thin_lto"].requires = ["pybind11_"]
        self.cpp_info.components["opt_size"].requires = ["pybind11_"]
        self.cpp_info.components["python2_no_register"].requires = ["pybind11_"]

        # ASWF FIXME: do we need this?
        self.env_info.CMAKE_PREFIX_PATH.append(os.path.join(self.package_folder, "lib64", "cmake"))
