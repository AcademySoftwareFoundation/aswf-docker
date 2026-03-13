# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, get, rm, rmdir
from conan.tools.microsoft import is_msvc, is_msvc_static_runtime
from conan.tools.scm import Version
from conan.errors import ConanInvalidConfiguration
import os

required_conan_version = ">=2.1"


class OpenShadingLanguageConan(ConanFile):
    name = "osl" # ASWF: short name for compatibility
    description = (
        "Open Shading Language (OSL) is a small but rich language for programmable "
        "shading in advanced renderers and other applications, ideal for describing "
        "materials, lights, displacement, and pattern generation."
    )
    topics = ("vfx", "image", "picture")
    license = "BSD-3-Clause"
    homepage = "https://github.com/AcademySoftwareFoundation/OpenShadingLanguage"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_optix": [True, False],
        "with_partio": [True, False],
        "with_python": [True, False],
        "with_qt": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_optix": True,
        "with_partio": True,
        "with_python": True,
        "with_qt": True,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        # FIXME need better way to determine llvm version
        self.requires(f"clang/{os.environ['ASWF_PYSIDE_CLANG_VERSION']}@{self.user}/ci_common{os.environ['CI_COMMON_VERSION']}")
        # Required libraries
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires("fmt/10.2.1", transitive_headers=True)
        self.requires("tsl-robin-map/1.2.1")
        self.requires("oiio/[>=2.5]")
        self.requires("imath/3.1.9", transitive_headers=True)
        if Version(self.version) <= "1.13":
            # OSL 1.13 has vestigial OpenEXR includes
            self.requires("openexr/[>=3.0.0]")
        self.requires("pugixml/[>=1.8]")
        if self.options.with_partio:
            self.requires("partio/[>=1.19.0]")
        if self.options.with_python:
            self.requires("cpython/[>=3.9]")
            self.requires("pybind11/2.7]")
        if self.options.with_qt:
            self.requires("qt/6.5.6")

    def build_requirements(self):
        # FIXME need better way to determine llvm version
        self.tool_requires(f"clang/{os.environ['ASWF_PYSIDE_CLANG_VERSION']}@{self.user}/ci_common{os.environ['CI_COMMON_VERSION']}")
        self.tool_requires("cmake/[>=3.19]")
        self.tool_requires("bison/[>=2.7]")
        self.tool_requires("flex/[>=2.5.35]")

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, 17)
        if is_msvc(self) and is_msvc_static_runtime(self) and self.options.shared:
            raise ConanInvalidConfiguration(
                "Building shared library with static runtime is not supported!"
            )

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)

        # CMake options
        tc.variables["CMAKE_CXX_STANDARD"] = self.settings.compiler.cppstd
        tc.variables["OSL_USE_OPTIX"] = self.options.with_optix
        tc.variables["USE_PARTIO"] = self.options.with_partio
        tc.variables["USE_PYTHON"] = self.options.with_python
        tc.variables["USE_QT"] = self.options.with_qt
        tc.variables["OPTIXHOME"] = "/usr/local/NVIDIA-OptiX-SDK-9.0.0" # ASWF FIXME
        if Version(self.version) <= "1.13":
            tc.variables["INSTALL_DOCS"] = "OFF" # skip documentation build

        tc.generate()
        cd = CMakeDeps(self)
        cd.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build(cli_args=["--verbose"])

    def package(self):
        # ASWF: license files in package subdirectory
        copy(self, "LICENSE*.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "share"))
        if self.settings.os == "Windows":
            for vc_file in ("concrt", "msvcp", "vcruntime"):
                rm(self, f"{vc_file}*.dll", os.path.join(self.package_folder, "bin"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        # ASWF: keep cmake for outside conan use
        # rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    @staticmethod
    def _conan_comp(name):
        return f"openimageio_{name.lower()}"

    def _add_component(self, name):
        component = self.cpp_info.components[self._conan_comp(name)]
        component.set_property("cmake_target_name", f"OpenImageIO::{name}")
        component.names["cmake_find_package"] = name
        component.names["cmake_find_package_multi"] = name
        return component

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenShadingLanguage")
        self.cpp_info.set_property("cmake_target_name", "OpenShadingLanguage::OpenShadingLanguage")
        self.cpp_info.set_property("pkg_config_name", "OpenOpenShadingLanguage")

        self.cpp_info.libs = ["oslcomp", "oslexec", "oslnoise", "oslquery", "osltestshade"]

        self.cpp_info.requires = [
            "clang::LLVM",
            "zlib::zlib",
            "fmt::fmt",
            "tsl-robin-map::tsl-robin-map",
            "oiio::OpenImageIO",
            "imath::imath",
            "pugixml::pugixml",
        ]
        if self.options.with_partio:
            self.cpp_info.requires.append("partio::partio")
        if self.options.with_python:
            self.cpp_info.requires.append("cpython::cpython")
            self.cpp_info.requires.append("pybind11::pybind11")
        if self.options.with_qt:
            # ASWF FIXME: may not need the whole thing
            self.cpp_info.requires.append("qt::qt")
