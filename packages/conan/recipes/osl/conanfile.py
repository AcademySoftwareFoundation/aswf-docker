# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualRunEnv
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
        self.requires(self.conf.get("user.aswf:osl_clang_ref", check_type=str))
        # Required libraries
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires("fmt/10.2.1", transitive_headers=True)
        self.requires("tsl-robin-map/1.2.1")
        self.requires("openimageio/[>=2.5]")
        self.requires("imath/3.1.9", transitive_headers=True)
        self.requires("pugixml/[>=1.8]")
        if self.options.with_partio:
            self.requires("partio/[>=1.19.0]")
        if self.options.with_python:
            self.requires("cpython/[>=3.9]")
            self.requires("pybind11/2.7]")
        if self.options.with_qt:
            self.requires("qt/6.5.6")

    def build_requirements(self):
        self.tool_requires(self.conf.get("user.aswf:osl_clang_ref", check_type=str))
        self.tool_requires("cmake/[>=3.19]")
        self.tool_requires("bison/[>=2.7]")
        self.tool_requires("flex/[>=2.5.35]")
        self.tool_requires("cpython/[>=3.0.0]") # used for bitfile generation

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
        if Version(self.version) < "1.14":
            tc.variables["INSTALL_DOCS"] = "OFF" # skip documentation build for 1.13 and older
        if Version(os.environ['ASWF_CUDA_VERSION']) >= "13": # ASWF FIXME: should have CUDA wrapper package
            tc.variables["CUDA_TARGET_ARCH"] = "sm_75" # CUDA 13 drops pre-Turing archs

        tc.generate()
        cd = CMakeDeps(self)
        cd.generate()
        # Host DSOs (Qt, HarfBuzz, …) must be on LD_LIBRARY_PATH when CMake runs oslc, etc.
        VirtualRunEnv(self).generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        # CMake.build() has no env= parameter (unlike self.run / CMake.ctest). Apply
        # VirtualRunEnv so cmake/configure and cmake --build child processes (oslc, …)
        # see LD_LIBRARY_PATH for host deps (Qt, HarfBuzz, …) before /usr/lib64.
        with VirtualRunEnv(self).vars().apply():
            cmake.configure()
            cmake.build()

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
        return f"osl_{name.lower()}"

    def _add_component(self, name):
        component = self.cpp_info.components[self._conan_comp(name)]
        component.set_property("cmake_target_name", f"OSL::{name}")
        component.names["cmake_find_package"] = name
        component.names["cmake_find_package_multi"] = name
        return component

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OSL")
        self.cpp_info.set_property("cmake_target_name", "OSL::OSL")
        self.cpp_info.set_property("pkg_config_name", "OSL")
        self.cpp_info.bindirs = ["bin"]

        # ASWF: split into per-library components (instead of one flat
        # OSL::OSL aggregate) so consumers like OpenUSD's sdrOsl plugin can
        # link a specific OSL library by name -- see
        # openusd's patches/*-cmake-packages.patch, which references
        # OSL::oslquery in place of the OSL_QUERY_LIBRARY variable that
        # OpenUSD's own FindOSL.cmake module would have set (ignored when
        # building with Conan, since CMakeDeps takes config mode over
        # OpenUSD's custom module). Conan still auto-generates the
        # aggregate OSL::OSL target linking all components together, so
        # existing consumers of the whole thing are unaffected.
        common_requires = [
            "clang::clang",
            "zlib::zlib",
            "fmt::fmt",
            "tsl-robin-map::tsl-robin-map",
            "openimageio::openimageio",
            "imath::imath",
            "pugixml::pugixml",
        ]
        if self.options.with_partio:
            common_requires.append("partio::partio")
        if self.options.with_python:
            common_requires.append("cpython::cpython")
            common_requires.append("pybind11::pybind11")
        if self.options.with_qt:
            # ASWF FIXME: may not need the whole thing
            common_requires.append("qt::qt")

        oslcomp = self._add_component("oslcomp")
        oslcomp.libs = ["oslcomp"]
        oslcomp.requires = common_requires

        oslexec = self._add_component("oslexec")
        oslexec.libs = ["oslexec"]
        oslexec.requires = common_requires

        oslnoise = self._add_component("oslnoise")
        oslnoise.libs = ["oslnoise"]
        oslnoise.requires = common_requires

        # ASWF: liboslquery only actually links OpenImageIO_Util (verified
        # against upstream src/liboslquery/CMakeLists.txt), so it's kept
        # deliberately minimal here rather than inheriting common_requires
        # -- consumers that only need shader metadata queries (like
        # sdrOsl) shouldn't be forced to also pull in clang/LLVM.
        oslquery = self._add_component("oslquery")
        oslquery.libs = ["oslquery"]
        oslquery.requires = ["openimageio::openimageio_openimageio_util"]

        testshade = self._add_component("testshade")
        testshade.libs = ["testshade"]
        testshade.requires = common_requires
