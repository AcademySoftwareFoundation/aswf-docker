# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import (
    apply_conandata_patches,
    copy,
    export_conandata_patches,
    get,
    rmdir,
)
from conan.tools.microsoft import is_msvc
import os
import subprocess

required_conan_version = ">=1.38.0"


class OpenSubdivConan(ConanFile):
    name = "opensubdiv"
    description = "An Open-Source subdivision surface library."
    topics = "conan", "opensubdiv", "vfx"
    homepage = "https://github.com/PixarAnimationStudios/OpenSubdiv"
    license = "Apache-2.0"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    settings = (
        "os",
        "arch",
        "compiler",
        "build_type",
    )
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_tbb": [True, False],
        "with_opengl": [True, False],
        "with_omp": [True, False],
        "with_cuda": [True, False],
        "with_clew": [True, False],
        "with_opencl": [True, False],
        "with_dx": [True, False],
        "with_metal": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_tbb": True,
        "with_opengl": True,
        "with_omp": False,
        "with_cuda": True,
        "with_clew": False,
        "with_opencl": False,
        "with_dx": False,
        "with_metal": False,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")
        # We want DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def requirements(self):
        if self.options.with_opengl:
            self.requires(
                f"glfw/{os.environ['ASWF_GLFW_VERSION']}@{self.user}/{self.channel}"
            )
            self.requires(
                f"glew/{os.environ['ASWF_GLEW_VERSION']}@{self.user}/{self.channel}"
            )
        if self.options.with_tbb:
            self.requires(
                f"tbb/{os.environ['ASWF_TBB_VERSION']}@{self.user}/{self.channel}"
            )

    def build_requirements(self):
        self.build_requires(
            f"cmake/{os.environ['ASWF_CMAKE_VERSION']}@{self.user}/{self.channel}"
        )

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    @property
    def _osd_gpu_enabled(self):
        return any(
            [
                self.options.with_opengl,
                self.options.with_opencl,
                self.options.with_cuda,
                self.options.get_safe("with_dx"),
                self.options.get_safe("with_metal"),
            ]
        )

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["NO_TBB"] = not self.options.with_tbb
        tc.variables["NO_OPENGL"] = not self.options.with_opengl
        tc.variables["BUILD_SHARED_LIBS"] = self.options.get_safe("shared")
        tc.variables["NO_OMP"] = not self.options.with_omp
        tc.variables["NO_CUDA"] = not self.options.with_cuda
        tc.variables["NO_DX"] = not self.options.get_safe("with_dx")
        tc.variables["NO_METAL"] = not self.options.get_safe("with_metal")
        tc.variables["NO_CLEW"] = not self.options.with_clew
        tc.variables["NO_OPENCL"] = not self.options.with_opencl
        tc.variables[
            "NO_PTEX"
        ] = True  # Note: PTEX is for examples only, but we skip them..
        tc.variables["NO_DOC"] = True
        tc.variables["NO_EXAMPLES"] = True
        tc.variables["NO_TUTORIALS"] = True
        tc.variables["NO_REGRESSION"] = True
        tc.variables["NO_TESTS"] = True
        tc.variables["NO_GLTESTS"] = True
        tc.variables["NO_MACOS_FRAMEWORK"] = True
        tc.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(
            self,
            "LICENSE.txt",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses", self.name),
        )
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))
        if self.options.shared:
            rm(self, "*.a", os.path.join(self.package_folder, "lib"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenSubdiv")
        target_suffix = "" if self.options.shared else "_static"

        self.cpp_info.components["osdcpu"].set_property(
            "cmake_target_name", f"OpenSubdiv::osdcpu{target_suffix}"
        )
        self.cpp_info.components["osdcpu"].libs = ["osdCPU"]
        if self.options.with_tbb:
            self.cpp_info.components["osdcpu"].requires = ["tbb::tbb"]

        if self._osd_gpu_enabled:
            self.cpp_info.components["osdgpu"].set_property(
                "cmake_target_name", f"OpenSubdiv::osdgpu{target_suffix}"
            )
            self.cpp_info.components["osdgpu"].libs = ["osdGPU"]
            dl_required = self.options.with_opengl or self.options.with_opencl
            if self.settings.os in ["Linux", "FreeBSD"] and dl_required:
                self.cpp_info.components["osdgpu"].system_libs = ["dl"]

        # TODO: to remove in conan v2
        self.cpp_info.names["cmake_find_package"] = "OpenSubdiv"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenSubdiv"
        self.cpp_info.components["osdcpu"].names[
            "cmake_find_package"
        ] = f"osdcpu{target_suffix}"
        self.cpp_info.components["osdcpu"].names[
            "cmake_find_package_multi"
        ] = f"osdcpu{target_suffix}"
        self.cpp_info.components["osdgpu"].names[
            "cmake_find_package"
        ] = f"osdgpu{target_suffix}"
        self.cpp_info.components["osdgpu"].names[
            "cmake_find_package_multi"
        ] = f"osdgpu{target_suffix}"

    def deploy(self):
        self.copy("*", symlinks=True)
