# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/2a3cb93885141024c1b405a01a79fb3abc239b12/recipes/materialx/all/conanfile.py

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rm, rmdir, replace_in_file
from conan.tools.apple import is_apple_os
from conan.tools.scm import Version
import os

required_conan_version = ">=1.53.0"

class MaterialXConan(ConanFile):
    name = "materialx"
    description = "MaterialX is an open standard for the exchange of rich material and look-development content across applications and renderers."
    license = "Apache-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/AcademySoftwareFoundation/MaterialX"
    topics = ("vfx", "3d", "graphics", "aswf")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_openimageio": [True, False],
        "build_gen_msl": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_openimageio": True, # ASWF: exercise dependency
        "build_gen_msl": True
    }

    short_paths = True

    @property
    def _min_cppstd(self):
        if Version(self.version) >= "1.39.0":
            return 17
        else:
            return 14

    @property
    def _compilers_minimum_version(self):
        return {
            "apple-clang": "10",
            "clang": "7",
            "gcc": "7",
            "msvc": "191",
            "Visual Studio": "15",
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
        # ASWF: DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def requirements(self):
        if self.options.with_openimageio:
            self.requires(f"oiio/{os.environ['ASWF_OIIO_VERSION']}@{self.user}/{self.channel}") # ASWF: oiio backwards compatibility
        self.requires(f"cpython/{os.environ['ASWF_CPYTHON_VERSION']}@{self.user}/{self.channel}")
        # Comment out to use vendored pybind11
        self.requires(f"pybind11/{os.environ['ASWF_PYBIND11_VERSION']}@{self.user}/{self.channel}")
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.requires("xorg/system")
            self.requires("opengl/system")

    def validate(self):
        # validate the minimum cpp standard supported. For C++ projects only
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, self._min_cppstd)
        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if minimum_version and Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(
                f"{self.ref} requires C++{self._min_cppstd}, which your compiler does not support."
            )

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.24 <4]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["MATERIALX_BUILD_TESTS"] = False
        tc.variables["MATERIALX_TEST_RENDER"] = False
        tc.variables["MATERIALX_BUILD_PYTHON"] = "ON"
        tc.variables["MATERIALX_PYTHON_VERSION"] = os.environ["ASWF_CPYTHON_VERSION"]
        tc.variables["MATERIALX_BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["MATERIALX_BUILD_GEN_MSL"] = self.options.build_gen_msl and is_apple_os
        tc.variables["MATERIALX_INSTALL_LIB_PATH"] = "lib64" # ASWF: otherwise end up in lib
        tc.variables["MATERIALX_INSTALL_STDLIB_PATH"] = os.path.join("share","MaterialX") # ASWF: otherwise end up in python
        # TODO: Remove when Conan 1 support is dropped
        if not self.settings.compiler.cppstd:
            tc.variables["MATERIALX_BUILD_USE_CCACHE"] = self._min_cppstd
        tc.variables["MATERIALX_BUILD_USE_CCACHE"] = False
        tc.generate()

        tc = CMakeDeps(self)
        tc.generate()

    def _patch_sources(self):
        apply_conandata_patches(self) # ASWF: we have external patches
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"),
                        "set(CMAKE_CXX_STANDARD",
                        "# set(CMAKE_CXX_STANDARD")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"),
                        "set(CMAKE_POSITION_INDEPENDENT_CODE",
                        "# set(CMAKE_POSITION_INDEPENDENT_CODE")

    def build(self):
        self._patch_sources() # ASWF: don't forget to patch sources
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # ASWF: license files in package subdirs
        copy(self, "LICENSE.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()

        rmdir(self, os.path.join(self.package_folder, "resources"))
        rmdir(self, os.path.join(self.package_folder, "libraries"))
        # ASWF: keep CMake modules
        # rmdir(self, os.path.join(self.package_folder, "lib64", "cmake"))
        rm(self, "README.md", self.package_folder)
        rm(self, "CHANGELOG.md", self.package_folder)
        rm(self, "THIRD-PARTY.md", self.package_folder)
        rm(self, "LICENSE", self.package_folder)    
        # ASWF: libraries in lib64
        rm(self, "*.la", os.path.join(self.package_folder, "lib64"))
        rm(self, "*.pdb", os.path.join(self.package_folder, "lib64"))
        rm(self, "*.pdb", os.path.join(self.package_folder, "bin"))

    def package_info(self):
        self.cpp_info.requires.append("cpython::cpython")
        # You can try uncommenting the following to use vendored pybind11
        # instead of Conan dependency
        self.cpp_info.requires.append("pybind11::pybind11")
        #self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "python"))

        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("m")
            self.cpp_info.system_libs.append("dl")

        self.cpp_info.components["MaterialXCore"].libs = ["MaterialXCore"]

        self.cpp_info.components["MaterialXFormat"].libs = ["MaterialXFormat"]
        self.cpp_info.components["MaterialXFormat"].requires = ["MaterialXCore"]

        self.cpp_info.components["MaterialXGenGlsl"].libs = ["MaterialXGenGlsl"]
        self.cpp_info.components["MaterialXGenGlsl"].requires = ["MaterialXCore", "MaterialXGenShader"]

        self.cpp_info.components["MaterialXGenMdl"].libs = ["MaterialXGenMdl"]
        self.cpp_info.components["MaterialXGenMdl"].requires = ["MaterialXCore", "MaterialXGenShader"]

        self.cpp_info.components["MaterialXGenMsl"].libs = ["MaterialXGenMsl"]
        self.cpp_info.components["MaterialXGenMsl"].requires = ["MaterialXCore", "MaterialXGenShader"]

        self.cpp_info.components["MaterialXGenOsl"].libs = ["MaterialXGenOsl"]
        self.cpp_info.components["MaterialXGenOsl"].requires = ["MaterialXCore", "MaterialXGenShader"]

        self.cpp_info.components["MaterialXGenShader"].libs = ["MaterialXGenShader"]
        self.cpp_info.components["MaterialXGenShader"].requires = ["MaterialXCore", "MaterialXFormat"]

        self.cpp_info.components["MaterialXRender"].libs = ["MaterialXRender"]
        self.cpp_info.components["MaterialXRender"].requires = ["MaterialXGenShader"]
        if self.options.with_openimageio:
            self.cpp_info.components["MaterialXRender"].requires.append("oiio::OpenImageIO") # ASWF: Conan package named oiio

        self.cpp_info.components["MaterialXRenderGlsl"].libs = ["MaterialXRenderGlsl"]
        self.cpp_info.components["MaterialXRenderGlsl"].requires = ["MaterialXRenderHw", "MaterialXGenGlsl"]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["MaterialXRenderGlsl"].requires.append("opengl::opengl")
        elif self.settings.os in ["Macos", "iOS"]:
            self.cpp_info.frameworks.extend(["Foundation", "Cocoa", "OpenGL"])
            if self.settings.os == "Macos":
                self.cpp_info.includedirs.extend(["include/compat/osx"])
            else:
                self.cpp_info.includedirs.extend(["include/compat/ios"])
        elif self.settings.os == "Windows":
            self.cpp_info.system_libs.append("opengl32")

        self.cpp_info.components["MaterialXRenderHw"].libs = ["MaterialXRenderHw"]
        self.cpp_info.components["MaterialXRenderHw"].requires = ["MaterialXRender"]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["MaterialXRenderHw"].requires.append("xorg::xorg")
        elif self.settings.os in ["Macos", "iOS"]:
            self.cpp_info.frameworks.extend(["Foundation", "Cocoa", "AppKit", "Metal"])
            if self.settings.os == "Macos":
                self.cpp_info.includedirs.extend(["include/compat/osx"])
            else:
                self.cpp_info.includedirs.extend(["include/compat/ios"])

        self.cpp_info.components["MaterialXRenderOsl"].libs = ["MaterialXRenderOsl"]
        self.cpp_info.components["MaterialXRenderOsl"].requires = ["MaterialXRender"]

        if self.options.build_gen_msl:
            self.cpp_info.components["MaterialXGenMsl"].libs = ["MaterialXGenMsl"]
            self.cpp_info.components["MaterialXGenMsl"].requires = ["MaterialXCore", "MaterialXGenShader"]
            
        if self.options.build_gen_msl and self.settings.os == "Macos":
            self.cpp_info.components["MaterialXRenderMsl"].libs = ["MaterialXRenderMsl"]
            self.cpp_info.components["MaterialXRenderMsl"].requires = ["MaterialXRenderHw", "MaterialXGenMsl"]
            self.cpp_info.frameworks.extend(["CoreFoundation", "OpenGL", "AppKit", "Metal"])
            if self.settings.os == "Macos":
                self.cpp_info.includedirs.extend(["include/compat/osx"])
            else:
                self.cpp_info.includedirs.extend(["include/compat/ios"])

        # ASWF FIXME still need this?
        self.env_info.CMAKE_PREFIX_PATH.append(os.path.join(self.package_folder, "lib64", "cmake"))
