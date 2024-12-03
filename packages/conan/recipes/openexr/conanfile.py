# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/cceee569179c10fa56d1fd9c3582f3371944ba59/recipes/openexr/3.x/conanfile.py

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, get, rmdir, replace_in_file
from conan.tools.scm import Version
import os

required_conan_version = ">=1.53.0"


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
        "shared": True, # ASWF: build shared libraries
        "fPIC": True,
    }

    @property
    def _min_cppstd(self):
        if Version(self.version) >= "3.3":
            return 17
        return 11

    @property
    def _minimum_compiler_version(self):
        return {
            "17": {
                "gcc": "9"
            }
        }.get(str(self._min_cppstd), {})

    @property
    def _with_libdeflate(self):
        return Version(self.version) >= "3.2"

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

    def requirements(self):
        self.requires("zlib/[>=1.2.11 <2]")
        # Note: OpenEXR and Imath are versioned independently.
        self.requires(f"imath/{os.environ['ASWF_IMATH_VERSION']}@{self.user}/{self.channel}")
        if self._with_libdeflate:
            self.requires("libdeflate/1.19")
        self.requires(f"cpython/{os.environ['ASWF_CPYTHON_VERSION']}@{self.user}/{self.channel}")
        self.requires(f"boost/{os.environ['ASWF_BOOST_VERSION']}@{self.user}/{self.channel}")

    def build_requirements(self):
        self.build_requires(f"cmake/{os.environ['ASWF_CMAKE_VERSION']}@{self.user}/{self.channel}")

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)

        minimum_version = self._minimum_compiler_version.get(str(self.settings.compiler))
        if minimum_version and Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(f"{self.ref} requires {self.settings.compiler} >= {minimum_version}")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["OPENEXR_BUILD_PYTHON_LIBS"] = "ON"
        tc.variables["OPENEXR_INSTALL_EXAMPLES"] = False
        tc.variables["BUILD_TESTING"] = False
        tc.variables["BUILD_WEBSITE"] = False
        tc.variables["DOCS"] = False
        tc.generate()
        cd = CMakeDeps(self)
        cd.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

        if Version(self.version) >= "3.2":
            # Even with BUILD_WEBSITE, Website target is compiled in 3.2
            replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"),
                            "add_subdirectory(website/src)",
                            "#  add_subdirectory(website/src)")

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
        # ASWF: modules in lib64, keep cmake for non-Conan clients
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))
        # rmdir(self, os.path.join(self.package_folder, "lib64", "cmake"))

    @staticmethod
    def _conan_comp(name):
        return f"openexr_{name.lower()}"

    def _add_component(self, name):
        component = self.cpp_info.components[self._conan_comp(name)]
        component.set_property("cmake_target_name", f"OpenEXR::{name}")
        component.names["cmake_find_package"] = name
        component.names["cmake_find_package_multi"] = name
        return component

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenEXR")
        self.cpp_info.set_property("pkg_config_name", "OpenEXR")

        self.cpp_info.names["cmake_find_package"] = "OpenEXR"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenEXR"
        self.cpp_info.names["pkg_config"] = "OpenEXR"

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
        if self._with_libdeflate:
            OpenEXRCore.requires.append("libdeflate::libdeflate")
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

        # Add tools directory to PATH
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))

        # ASWF FIXME: do we still need this?
        # self.cpp_info.requires.append("python::PythonLibs")
        # self.cpp_info.requires.append("boost::python")
        #
        # pymajorminor = self.deps_user_info["python"].python_interp
        # self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib64", pymajorminor, "site-packages"))
        # self.env_info.CMAKE_PREFIX_PATH.append(os.path.join(self.package_folder, "lib64", "cmake"))
