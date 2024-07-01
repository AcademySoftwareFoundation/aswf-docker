# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import (
    apply_conandata_patches,
    collect_libs,
    copy,
    export_conandata_patches,
    get,
    rmdir,
)
from conan.tools.microsoft import is_msvc
from conan.tools.scm import Version
from conans import tools, RunEnvironment
import os

required_conan_version = ">=1.38.0"


class ImathConan(ConanFile):
    name = "imath"
    description = "Imath is a C++ and python library of 2D and 3D vector, matrix, and math operations for computer graphics."
    topics = "conan", "imath", "python", "vfx"
    homepage = "https://github.com/AcademySoftwareFoundation/Imath"
    license = "BSD-3-Clause"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    settings = (
        "os",
        "arch",
        "compiler",
        "build_type",
        "python",
    )

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")
        # We want DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def requirements(self):
        self.requires(
            f"python/{os.environ['ASWF_PYTHON_VERSION']}@{self.user}/{self.channel}"
        )
        self.requires(
            f"boost/{os.environ['ASWF_BOOST_VERSION']}@{self.user}/{self.channel}"
        )

    def build_requirements(self):
        self.build_requires(
            f"cmake/{os.environ['ASWF_CMAKE_VERSION']}@{self.user}/{self.channel}"
        )

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        # Build Python bindings
        tc.variables["PYTHON"] = "ON"
        # FIXME: Python_ROOT and Boost_ROOT required to find Conan-installed packages?
        tc.cache_variables["Python_ROOT"] = self.deps_cpp_info["python"].rootpath
        tc.cache_variables["Boost_ROOT"] = self.deps_cpp_info["boost"].rootpath
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            self._patch_sources()
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def package(self):
        copy(
            self,
            "LICENSE.md",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses", self.name),
        )
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))

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

        self.cpp_info.requires.append("python::PythonLibs")
        self.cpp_info.requires.append("boost::python")
        pymajorminor = self.deps_user_info["python"].python_interp
        self.env_info.PYTHONPATH.append(
            os.path.join(self.package_folder, "lib64", pymajorminor, "site-packages")
        )
        self.env_info.CMAKE_PREFIX_PATH.append(
            os.path.join(self.package_folder, "lib64", "cmake")
        )

    def deploy(self):
        self.copy("*", symlinks=True)
