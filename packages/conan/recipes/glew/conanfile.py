# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/22dfbd2b42eed730eca55e14025e8ffa65f723b2/recipes/glew/all/conanfile.py

from conan import ConanFile
from conan.tools.apple import is_apple_os
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rm, rmdir
import os

required_conan_version = ">=1.53.0"


class GlewConan(ConanFile):
    name = "glew"
    description = "The GLEW library"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://github.com/nigels-com/glew"
    topics = ("glew", "opengl", "wrangler", "loader", "binding")
    license = "MIT"
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_egl": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_egl": False,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            del self.options.with_egl

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")

    def layout(self):
        cmake_layout(self, src_folder="src")
        # ASWF: DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def requirements(self):
        self.requires("opengl/system")
        # GL/glew.h includes glu.h.
        if is_apple_os(self) or self.settings.os == "Windows":
            self.requires("glu/system", transitive_headers=True)
        else:
            # Don't depend on external GLU recipe
            # self.requires("mesa-glu/9.0.0", transitive_headers=True)
            self.requires("glu/system", transitive_headers=True)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_UTILS"] = False
        tc.variables["GLEW_EGL"] = self.options.get_safe("with_egl", False)
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, "build", "cmake"))
        cmake.build()

    def package(self):
        # ASWF: licenses in package subdirs
        copy(self, "LICENSE.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()

        # ASWF: libraries and cmake modules in lib64 
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))
        # ASWF: Keep CMake files to package can be consumed outside Conan
        # rmdir(self, os.path.join(self.package_folder, "lib64", "cmake"))
        rm(self, "*.pdb", os.path.join(self.package_folder, "lib64"))

    def package_info(self):
        glewlib_target_name = "glew" if self.options.shared else "glew_s"
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_module_file_name", "GLEW")
        self.cpp_info.set_property("cmake_file_name", "glew")
        self.cpp_info.set_property("cmake_target_name", "GLEW::GLEW")
        self.cpp_info.set_property("pkg_config_name", "glew")
        self.cpp_info.components["glewlib"].set_property("cmake_module_target_name", "GLEW::GLEW")
        self.cpp_info.components["glewlib"].set_property("cmake_target_name", f"GLEW::{glewlib_target_name}")
        self.cpp_info.components["glewlib"].set_property("pkg_config_name", "glew")

        if self.settings.os == "Windows":
            lib_name = "glew32" if self.options.shared else "libglew32"
        else:
            lib_name = "GLEW"
        if self.settings.build_type == "Debug":
            lib_name += "d"
        self.cpp_info.components["glewlib"].libs = [lib_name]
        if self.settings.os == "Windows" and not self.options.shared:
            self.cpp_info.components["glewlib"].defines.append("GLEW_STATIC")
        self.cpp_info.components["glewlib"].requires = ["opengl::opengl"]

        if is_apple_os(self) or self.settings.os == "Windows":
           self.cpp_info.components["glewlib"].requires.append("glu::glu")
        else:
           # Use system GLU
           # self.cpp_info.components["glewlib"].requires.append("mesa-glu::mesa-glu")
           self.cpp_info.components["glewlib"].requires.append("glu::glu")

        # TODO: to remove in conan v2 once cmake_find_package_* generators removed
        self.cpp_info.filenames["cmake_find_package"] = "GLEW"
        self.cpp_info.filenames["cmake_find_package_multi"] = "glew"
        self.cpp_info.names["cmake_find_package"] = "GLEW"
        self.cpp_info.names["cmake_find_package_multi"] = "GLEW"
        self.cpp_info.components["glewlib"].names["cmake_find_package"] = "GLEW"
        self.cpp_info.components["glewlib"].names["cmake_find_package_multi"] = glewlib_target_name

        self.env_info.CMAKE_PREFIX_PATH.append(
            os.path.join(self.package_folder, "lib64", "cmake")
        )
