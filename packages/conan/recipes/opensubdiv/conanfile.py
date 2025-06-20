# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/2a3cb93885141024c1b405a01a79fb3abc239b12/recipes/opensubdiv/all/conanfile.py

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd, valid_min_cppstd
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, replace_in_file, rm, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">=1.54.0"


class OpenSubdivConan(ConanFile):
    name = "opensubdiv"
    license = "LicenseRef-LICENSE.txt"
    homepage = "https://github.com/PixarAnimationStudios/OpenSubdiv"
    url = "https://github.com/conan-io/conan-center-index"
    description = "An Open-Source subdivision surface library"
    topics = ("cgi", "vfx", "animation", "subdivision surface")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
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
        "with_tbb": True, # ASWF
        "with_opengl": True, # ASWF
        "with_omp": False,
        "with_cuda": True, # ASWF
        "with_clew": False,
        "with_opencl": False,
        "with_dx": False,
        "with_metal": False,
    }

    short_paths = True

    @property
    def _min_cppstd(self):
        if self.options.get_safe("with_metal"):
            return "14"
        return "11"

    @property
    def _minimum_compilers_version(self):
        return {
            "Visual Studio": "15",
            "msvc": "191",
            "gcc": "5",
            "clang": "11",
            "apple-clang": "11.0",
        }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        else:
            del self.options.with_dx
        if self.settings.os != "Macos":
            del self.options.with_metal

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")
        # ASWF: DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def requirements(self):
        if self.options.with_opengl:
            self.requires(f"glfw/{os.environ['ASWF_GLFW_VERSION']}@{self.user}/{self.channel}")
            self.requires(f"glew/{os.environ['ASWF_GLEW_VERSION']}@{self.user}/{self.channel}")
        if self.options.with_tbb:
            # OpenSubdiv < 3.6.0 support only onettbb/2020.x.x
            # https://github.com/PixarAnimationStudios/OpenSubdiv/pull/1317
            if Version(self.version) < "3.6.0":
                self.requires("onetbb/2020.3.3", transitive_headers=True)
            else:
                self.requires("onetbb/2021.10.0", transitive_headers=True)

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
        if not valid_min_cppstd(self, self._min_cppstd):
            tc.variables["CMAKE_CXX_STANDARD"] = self._min_cppstd
        tc.variables["NO_TBB"] = not self.options.with_tbb
        tc.variables["NO_OPENGL"] = not self.options.with_opengl
        tc.variables["BUILD_SHARED_LIBS"] = self.options.get_safe("shared")
        tc.variables["NO_OMP"] = not self.options.with_omp
        tc.variables["NO_CUDA"] = not self.options.with_cuda
        tc.variables["NO_DX"] = not self.options.get_safe("with_dx")
        tc.variables["NO_METAL"] = not self.options.get_safe("with_metal")
        tc.variables["NO_CLEW"] = not self.options.with_clew
        tc.variables["NO_OPENCL"] = not self.options.with_opencl
        tc.variables["NO_PTEX"] = True  # Note: PTEX is for examples only, but we skip them..
        tc.variables["NO_DOC"] = True
        tc.variables["NO_EXAMPLES"] = True
        tc.variables["NO_TUTORIALS"] = True
        tc.variables["NO_REGRESSION"] = True
        tc.variables["NO_TESTS"] = True
        tc.variables["NO_GLTESTS"] = True
        tc.variables["NO_MACOS_FRAMEWORK"] = True
        tc.variables["CMAKE_LIBDIR_BASE"] = "lib64" # ASWF: DSOs in lib64
        tc.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)
        if self.settings.os == "Macos" and not self._osd_gpu_enabled:
            path = os.path.join(self.source_folder, "opensubdiv", "CMakeLists.txt")
            replace_in_file(self, path, "$<TARGET_OBJECTS:osd_gpu_obj>", "")
        # No warnings as errors
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "/WX", "")

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        # ASWF: https://github.com/PixarAnimationStudios/OpenSubdiv/issues/1313
        # CUDA build fails with high parallelism, limit to 16 threads
        # seems to help
        cmake.build(cli_args=["--parallel","4"])

    def package(self):
        # ASWF: license files in package subdir
        copy(self, "LICENSE.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))
        if self.options.shared:
            # ASWF: libraries in lib64
            # ASWF: OpenSubDiv cmake set up for both static and dynamic, downstream consummers unhappy
            # if static libs are missing
            # rm(self, "*.a", os.path.join(self.package_folder, "lib64"))
            pass

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenSubdiv")
        target_suffix = "" if self.options.shared else "_static"

        self.cpp_info.components["osdcpu"].set_property("cmake_target_name", f"OpenSubdiv::osdcpu{target_suffix}")
        self.cpp_info.components["osdcpu"].libs = ["osdCPU"]
        if self.options.with_tbb:
            self.cpp_info.components["osdcpu"].requires = ["onetbb::onetbb"]

        if self._osd_gpu_enabled:
            self.cpp_info.components["osdgpu"].set_property("cmake_target_name", f"OpenSubdiv::osdgpu{target_suffix}")
            self.cpp_info.components["osdgpu"].libs = ["osdGPU"]
            dl_required = self.options.with_opengl or self.options.with_opencl
            if self.settings.os in ["Linux", "FreeBSD"] and dl_required:
                self.cpp_info.components["osdgpu"].system_libs = ["dl"]
            # ASWF: building with_opengl
            if self.options.with_opengl:
               self.cpp_info.components["osdgpu"].requires = ["glew::glew", "glfw::glfw"]

        # TODO: to remove in conan v2
        self.cpp_info.names["cmake_find_package"] = "OpenSubdiv"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenSubdiv"
        self.cpp_info.components["osdcpu"].names["cmake_find_package"] = f"osdcpu{target_suffix}"
        self.cpp_info.components["osdcpu"].names["cmake_find_package_multi"] = f"osdcpu{target_suffix}"
        self.cpp_info.components["osdgpu"].names["cmake_find_package"] = f"osdgpu{target_suffix}"
        self.cpp_info.components["osdgpu"].names["cmake_find_package_multi"] = f"osdgpu{target_suffix}"
