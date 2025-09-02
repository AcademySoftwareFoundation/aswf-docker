# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5f19361f49bc31a349b383c1f95c7f79627f728a/recipes/eigen/all/conanfile.py

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, cmake_layout, CMakeToolchain
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, get, rmdir
import os
import re

required_conan_version = ">=1.52.0"


class EigenConan(ConanFile):
    name = "eigen"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://eigen.tuxfamily.org"
    description = "Eigen is a C++ template library for linear algebra: matrices, vectors," \
                  " numerical solvers, and related algorithms."
    topics = ("algebra", "linear-algebra", "matrix", "vector", "numerical", "header-only")
    package_type = "header-library"
    license = ("MPL-2.0", "LGPL-3.0-or-later")  # Taking into account the default value of MPL2_only option

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "MPL2_only": [True, False],
    }
    default_options = {
        "MPL2_only": False,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def configure(self):
        self.license = "MPL-2.0" if self.options.MPL2_only else ("MPL-2.0", "LGPL-3.0-or-later")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
            destination=self.source_folder, strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["BUILD_TESTING"] = not self.conf.get("tools.build:skip_test", default=True, check_type=bool)
        tc.cache_variables["EIGEN_TEST_NOQT"] = True
        tc.generate()

        deps = CMakeDeps(self) # ASWF: CMake dependencies generator
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        # ASWF: license files in package specific directories
        copy(self, "COPYING.*", self.source_folder, os.path.join(self.package_folder, "licenses", self.name))
        rmdir(self, os.path.join(self.package_folder, "share"))

        # ASWF: package CMake files even though this is a header-library
        target_dir = os.path.join(self.package_folder, "lib", "cmake", "Eigen3")
        copy(self, "Eigen3Config.cmake", self.build_folder, target_dir)
        copy(self, "Eigen3ConfigVersion.cmake", self.build_folder, target_dir)
        copy(self, "Eigen3Targets.cmake", self.build_folder, target_dir)
        # ASWF: since conan install is not processing these files, bake desired path
        eigen3targets = os.path.join(target_dir,"Eigen3Targets.cmake")
        with open(eigen3targets, 'r') as f:
            file_data = f.read()
        updated_data = re.sub(r"\/opt\/conan_home\/d\/b\/eigen[0-9a-f]{13}\/b\/src","/usr/local/include/eigen3", file_data)
        with open(eigen3targets, 'w') as f:
            f.write(updated_data)

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Eigen3")
        self.cpp_info.set_property("cmake_target_name", "Eigen3::Eigen")
        self.cpp_info.set_property("pkg_config_name", "eigen3")
        # TODO: back to global scope once cmake_find_package* generators removed
        self.cpp_info.components["eigen3"].bindirs = []
        self.cpp_info.components["eigen3"].libdirs = []
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["eigen3"].system_libs = ["m"]
        if self.options.MPL2_only:
            self.cpp_info.components["eigen3"].defines = ["EIGEN_MPL2_ONLY"]

        # TODO: to remove in conan v2 once cmake_find_package* & pkg_config generators removed
        self.cpp_info.names["cmake_find_package"] = "Eigen3"
        self.cpp_info.names["cmake_find_package_multi"] = "Eigen3"
        self.cpp_info.names["pkg_config"] = "eigen3"
        self.cpp_info.components["eigen3"].names["cmake_find_package"] = "Eigen"
        self.cpp_info.components["eigen3"].names["cmake_find_package_multi"] = "Eigen"
        self.cpp_info.components["eigen3"].set_property("cmake_target_name", "Eigen3::Eigen")
        self.cpp_info.components["eigen3"].includedirs = [os.path.join("include", "eigen3")]
