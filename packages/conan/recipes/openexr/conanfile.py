# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/1ce15d41e0301e69706f20bf3d6d942221d8baae/recipes/openexr/3.x/conanfile.py

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, get, rmdir, replace_in_file
from conan.tools.scm import Version
import os

required_conan_version = ">=2.0"


class OpenEXRConan(ConanFile):
    name = "openexr"
    description = "OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial Light & " \
                  "Magic for use in computer imaging applications."
    license = "BSD-3-Clause"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/AcademySoftwareFoundation/openexr"
    topics = ("openexr", "hdr", "image", "picture")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
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

    def requirements(self):
        self.requires("zlib/[>=1.2.11 <2]")
        # Note: OpenEXR and Imath are versioned independently.
        self.requires("imath/[>=3.1.9 <4]", transitive_headers=True)
        if Version(self.version) >= "3.2": # ASWF: we still support pre-libdeflate 3.1.x
            self.requires("libdeflate/[>=1.19 <2]", transitive_libs=True) # ASWF: otherwise linked looks at system libdeflate
        # ASWF: OpenEXR 3.2 adds Python bindings
        if Version(self.version) >= "3.2":
            self.requires("cpython/[>=3.0.0]", visible=False)
        # ASWF: Starting with 3.3 they use pybind11
        if Version(self.version) >= "3.3":
            self.requires("pybind11/[>=2.0.0]", visible=False)

        if Version(self.version) >= "3.4":
            self.requires("openjph/[>=0.23.1 <1]")

    def validate(self):
        check_min_cppstd(self, 11)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["OPENEXR_BUILD_PYTHON"] = True # ASWF Build Python bindings
        tc.variables["OPENEXR_INSTALL_EXAMPLES"] = False
        tc.variables["BUILD_TESTING"] = False
        tc.variables["BUILD_WEBSITE"] = False
        tc.variables["DOCS"] = False
        tc.generate()

        cd = CMakeDeps(self)
        cd.set_property("openjph", "cmake_target_name", "openjph")
        cd.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

        if Version(self.version) >= "3.2":
            # Even with BUILD_WEBSITE, Website target is compiled in 3.2
            replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"),
                            "add_subdirectory(website/src)",
                            "#  add_subdirectory(website/src)")
            if Version(self.version) <= "3.4":
                # ASWF: use Python3 cmake namespace instead of unversioned Python so that
                # Conan's Python3Config.cmake (config mode) is used rather than FindPython.cmake
                # (module mode).  Config mode calls find_dependency for cpython's transitive
                # deps (EXPAT::EXPAT, ZLIB::ZLIB, etc.) before the targets file is included,
                # which avoids "target EXPAT::EXPAT not found" errors at cmake generate time.
                # 3.4.x already uses Python3 cmake symbols so no patching needed there.
                py_cmake = os.path.join(self.source_folder, "src", "wrappers", "python", "CMakeLists.txt")
                replace_in_file(self, py_cmake,
                                "find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)",
                                "find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)")
                replace_in_file(self, py_cmake,
                                "python_add_library (",
                                "python3_add_library (")
                replace_in_file(self, py_cmake,
                                '"${Python_LIBRARIES}"',
                                '"${Python3_LIBRARIES}"')

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # ASWF: licenses separate per package
        copy(self, "LICENSE.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "share"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        # rmdir(self, os.path.join(self.package_folder, "lib", "cmake")) # ASWF: keep cmake files

    @staticmethod
    def _conan_comp(name):
        return f"openexr_{name.lower()}"

    def _add_component(self, name):
        component = self.cpp_info.components[self._conan_comp(name)]
        component.set_property("cmake_target_name", f"OpenEXR::{name}")
        return component

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenEXR")
        self.cpp_info.set_property("pkg_config_name", "OpenEXR")

        lib_suffix = ""
        if not self.options.shared or self.settings.os == "Windows":
            openexr_version = Version(self.version)
            lib_suffix += f"-{openexr_version.major}_{openexr_version.minor}"
        if self.settings.build_type == "Debug":
            lib_suffix += "_d"

        # OpenEXR::OpenEXRConfig
        OpenEXRConfig = self._add_component("OpenEXRConfig")
        OpenEXRConfig.includedirs.append(os.path.join("include", "OpenEXR"))

        # OpenEXR::IexConfig
        IexConfig = self._add_component("IexConfig")
        IexConfig.includedirs = OpenEXRConfig.includedirs

        # OpenEXR::IlmThreadConfig
        IlmThreadConfig = self._add_component("IlmThreadConfig")
        IlmThreadConfig.includedirs = OpenEXRConfig.includedirs

        # OpenEXR::Iex
        Iex = self._add_component("Iex")
        Iex.libs = [f"Iex{lib_suffix}"]
        Iex.requires = [self._conan_comp("IexConfig")]
        if self.settings.os in ["Linux", "FreeBSD"]:
            Iex.system_libs = ["m"]

        # OpenEXR::IlmThread
        IlmThread = self._add_component("IlmThread")
        IlmThread.libs = [f"IlmThread{lib_suffix}"]
        IlmThread.requires = [
            self._conan_comp("IlmThreadConfig"), self._conan_comp("Iex"),
        ]
        if self.settings.os in ["Linux", "FreeBSD"]:
            IlmThread.system_libs = ["pthread", "m"]

        # OpenEXR::OpenEXRCore
        OpenEXRCore = self._add_component("OpenEXRCore")
        OpenEXRCore.libs = [f"OpenEXRCore{lib_suffix}"]
        OpenEXRCore.requires = [self._conan_comp("OpenEXRConfig"), "zlib::zlib"]
        if Version(self.version) >= "3.2": # ASWF: we still support pre-libdeflate 3.1.x
            OpenEXRCore.requires.append("libdeflate::libdeflate")
        if Version(self.version) >= "3.4":
            OpenEXRCore.requires.append("openjph::openjph")
        if self.settings.os in ["Linux", "FreeBSD"]:
            OpenEXRCore.system_libs = ["m"]

        # OpenEXR::OpenEXR
        OpenEXR = self._add_component("OpenEXR")
        OpenEXR.libs = [f"OpenEXR{lib_suffix}"]
        OpenEXR.requires = [
            self._conan_comp("OpenEXRCore"), self._conan_comp("IlmThread"),
            self._conan_comp("Iex"), "imath::imath",
        ]
        if self.settings.os in ["Linux", "FreeBSD"]:
            OpenEXR.system_libs = ["m"]

        # OpenEXR::OpenEXRUtil
        OpenEXRUtil = self._add_component("OpenEXRUtil")
        OpenEXRUtil.libs = [f"OpenEXRUtil{lib_suffix}"]
        OpenEXRUtil.requires = [self._conan_comp("OpenEXR")]
        if self.settings.os in ["Linux", "FreeBSD"]:
            OpenEXRUtil.system_libs = ["m"]

        # ASWF: OpenEXR::Python — Python bindings (PyOpenEXR.so, installed to site-packages).
        # No libs or includes exposed to consumers; this component exists solely to satisfy
        # Conan's requirement that every declared requires() appears in package_info, and to
        # keep cpython/pybind11 out of the main OpenEXR::OpenEXR cmake link interface.
        if Version(self.version) >= "3.2":
            openexr_python = self.cpp_info.components["openexr_python"]
            openexr_python.set_property("cmake_target_name", "OpenEXR::Python")
            openexr_python.libs = []
            openexr_python.libdirs = []
            openexr_python.includedirs = []
            openexr_python.requires = ["cpython::python"]
            if Version(self.version) >= "3.3":
                openexr_python.requires.append("pybind11::pybind11")

        # Add tools directory to PATH
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
