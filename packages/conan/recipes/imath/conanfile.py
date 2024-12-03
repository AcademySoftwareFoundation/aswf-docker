# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/cceee569179c10fa56d1fd9c3582f3371944ba59/recipes/imath/all/conanfile.py

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, collect_libs, copy, export_conandata_patches, get, rmdir
from conan.tools.microsoft import is_msvc
import os

required_conan_version = ">=1.53.0"


class ImathConan(ConanFile):
    name = "imath"
    description = (
        "Imath is a C++ and python library of 2D and 3D vector, matrix, and "
        "math operations for computer graphics."
    )
    license = "BSD-3-Clause"
    topics = ("computer-graphics", "matrix", "openexr", "3d-vector")
    homepage = "https://github.com/AcademySoftwareFoundation/Imath"
    url = "https://github.com/conan-io/conan-center-index"

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": True, # ASWF: build shared libraries
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
        # ASWF: We want DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, 11)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def requirements(self):
        self.requires(f"cpython/{os.environ['ASWF_CPYTHON_VERSION']}@{self.user}/{self.channel}")
        self.requires(f"boost/{os.environ['ASWF_BOOST_VERSION']}@{self.user}/{self.channel}")

    def build_requirements(self):
        self.build_requires(f"cmake/{os.environ['ASWF_CMAKE_VERSION']}@{self.user}/{self.channel}")

    def generate(self):
        tc = CMakeToolchain(self)
        if is_msvc(self) and self.settings.compiler.get_safe("cppstd"):
            # when msvc is working with a C++ standard level higher
            # than the default, we need the __cplusplus macro to be correct
            tc.variables["CMAKE_CXX_FLAGS"] = "/Zc:__cplusplus"
        # ASWF: Build Python bindings
        tc.variables["PYTHON"] = "ON"
        # ASWF: FIXME: Python_ROOT and Boost_ROOT required to find Conan-installed packages?
        # tc.cache_variables["Python_ROOT"] = self.deps_cpp_info["python"].rootpath
        # tc.cache_variables["Boost_ROOT"] = self.deps_cpp_info["boost"].rootpath
        tc.generate()

    def build(self):
        apply_conandata_patches(self)

        # ASWF FIXME: still need this?
        #env_build = RunEnvironment(self)
        #with tools.environment_append(env_build.vars):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # ASWF: separate licenses per package
        copy(self, "LICENSE.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        # ASWF: cmake modules in lib64, leave them for non-Conan builds
        # rmdir(self, os.path.join(self.package_folder, "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))
        # rmdir(self, os.path.join(self.package_folder, "lib64", "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Imath")
        self.cpp_info.set_property("cmake_target_name", "Imath::Imath")
        self.cpp_info.set_property("pkg_config_name", "Imath")

        # Imath::ImathConfig - header only library
        imath_config = self.cpp_info.components["imath_config"]
        imath_config.set_property("cmake_target_name", "Imath::ImathConfig")
        imath_config.includedirs.append(os.path.join("include", "Imath"))

        # Imath::Imath - linkable library
        imath_lib = self.cpp_info.components["imath_lib"]
        imath_lib.set_property("cmake_target_name", "Imath::Imath")
        imath_lib.set_property("pkg_config_name", "Imath")
        imath_lib.libs = collect_libs(self)
        imath_lib.requires = ["imath_config"]
        if self.settings.os == "Windows" and self.options.shared:
            imath_lib.defines.append("IMATH_DLL")

        # TODO: to remove in conan v2 once cmake_find_package_* generators removed
        self.cpp_info.names["cmake_find_package"] = "Imath"
        self.cpp_info.names["cmake_find_package_multi"] = "Imath"
        self.cpp_info.names["pkg_config"] = "Imath"
        imath_config.names["cmake_find_package"] = "ImathConfig"
        imath_config.names["cmake_find_package_multi"] = "ImathConfig"
        imath_lib.names["cmake_find_package"] = "Imath"
        imath_lib.names["cmake_find_package_multi"] = "Imath"
        imath_lib.names["pkg_config"] = "Imath"

        # FIXME ASWF: is this block still needed?
        # self.cpp_info.requires.append("cpython::PythonLibs")
        # self.cpp_info.requires.append("boost::python")
        #pymajorminor = self.deps_user_info["python"].python_interp
        #self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib64", pymajorminor, "site-packages"))
        # self.env_info.CMAKE_PREFIX_PATH.append(os.path.join(self.package_folder, "lib64", "cmake"))
