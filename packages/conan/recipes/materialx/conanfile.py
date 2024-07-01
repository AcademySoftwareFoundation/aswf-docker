# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conans import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import (
    apply_conandata_patches,
    copy,
    export_conandata_patches,
    get,
    rmdir,
)
from conan.tools.apple import is_apple_os
from conans import tools, RunEnvironment
import os

required_conan_version = ">=1.53.0"


class MaterialXConan(ConanFile):
    name = "materialx"
    description = "MaterialX is an open standard for the exchange of rich material and look-development content across applications and renderers."
    license = "Apache-2.0"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    homepage = "https://github.com/AcademySoftwareFoundation/MaterialX"
    topics = ("vfx", "3d", "graphics", "aswf")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type", "python"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_openimageio": [True, False],
        "build_gen_msl": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_openimageio": False,
        "build_gen_msl": True,
    }

    short_paths = True

    @property
    def _min_cppstd(self):
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
        # src_folder must use the same source folder name the project
        cmake_layout(self, src_folder="src")
        # We want DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def requirements(self):
        if self.options.with_openimageio:
            self.requires(
                f"openimageio/{os.environ['ASWF_OIIO_VERSION']}@{self.user}/{self.channel}"
            )
        self.requires(
            f"python/{os.environ['ASWF_PYTHON_VERSION']}@{self.user}/{self.channel}"
        )
        # Comment out to use vendored pybind11
        self.requires(
            f"pybind11/{os.environ['ASWF_PYBIND11_VERSION']}@{self.user}/{self.channel}"
        )
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.requires("xorg/system")
            self.requires("opengl/system")

    def build_requirements(self):
        self.build_requires(
            f"cmake/{os.environ['ASWF_CMAKE_VERSION']}@{self.user}/{self.channel}"
        )

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["MATERIALX_BUILD_TESTS"] = False
        tc.variables["MATERIALX_TEST_RENDER"] = False
        tc.variables["MATERIALX_BUILD_PYTHON"] = "ON"
        tc.variables["MATERIALX_PYTHON_VERSION"] = os.environ["ASWF_PYTHON_VERSION"]
        if self.options.shared:
            tc.variables["MATERIALX_BUILD_SHARED_LIBS"] = "ON"
        tc.variables["MATERIALX_BUILD_GEN_MSL"] = (
            self.options.build_gen_msl and is_apple_os
        )
        tc.generate()

    def build(self):
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            apply_conandata_patches(self)
            cmake = CMake(self)
            cmake.configure()
            cmake.build(cli_args=["--verbose"])
            # cmake.build()

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
        self.cpp_info.requires.append("python::PythonLibs")
        # You can try uncommenting the following to use vendored pybind11
        # instead of Conan dependency
        # self.cpp_info.requires.append("pybind11::main")
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "python"))

        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("m")
            self.cpp_info.system_libs.append("dl")

        self.cpp_info.components["MaterialXCore"].libs = ["MaterialXCore"]

        self.cpp_info.components["MaterialXFormat"].libs = ["MaterialXFormat"]
        self.cpp_info.components["MaterialXFormat"].requires = ["MaterialXCore"]

        self.cpp_info.components["MaterialXGenGlsl"].libs = ["MaterialXGenGlsl"]
        self.cpp_info.components["MaterialXGenGlsl"].requires = [
            "MaterialXCore",
            "MaterialXGenShader",
        ]

        self.cpp_info.components["MaterialXGenMdl"].libs = ["MaterialXGenMdl"]
        self.cpp_info.components["MaterialXGenMdl"].requires = [
            "MaterialXCore",
            "MaterialXGenShader",
        ]

        self.cpp_info.components["MaterialXGenMsl"].libs = ["MaterialXGenMsl"]
        self.cpp_info.components["MaterialXGenMsl"].requires = [
            "MaterialXCore",
            "MaterialXGenShader",
        ]

        self.cpp_info.components["MaterialXGenOsl"].libs = ["MaterialXGenOsl"]
        self.cpp_info.components["MaterialXGenOsl"].requires = [
            "MaterialXCore",
            "MaterialXGenShader",
        ]

        self.cpp_info.components["MaterialXGenShader"].libs = ["MaterialXGenShader"]
        self.cpp_info.components["MaterialXGenShader"].requires = [
            "MaterialXCore",
            "MaterialXFormat",
        ]

        self.cpp_info.components["MaterialXRender"].libs = ["MaterialXRender"]
        self.cpp_info.components["MaterialXRender"].requires = ["MaterialXGenShader"]
        if self.options.with_openimageio:
            self.cpp_info.components["MaterialXRender"].requires.append(
                "openimageio::openimageio"
            )

        self.cpp_info.components["MaterialXRenderGlsl"].libs = ["MaterialXRenderGlsl"]
        self.cpp_info.components["MaterialXRenderGlsl"].requires = [
            "MaterialXRenderHw",
            "MaterialXGenGlsl",
        ]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["MaterialXRenderGlsl"].requires.append(
                "opengl::opengl"
            )
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
            self.cpp_info.components["MaterialXGenMsl"].requires = [
                "MaterialXCore",
                "MaterialXGenShader",
            ]

        if self.options.build_gen_msl and self.settings.os == "Macos":
            self.cpp_info.components["MaterialXRenderMsl"].libs = ["MaterialXRenderMsl"]
            self.cpp_info.components["MaterialXRenderMsl"].requires = [
                "MaterialXRenderHw",
                "MaterialXGenMsl",
            ]
            self.cpp_info.frameworks.extend(
                ["CoreFoundation", "OpenGL", "AppKit", "Metal"]
            )
            if self.settings.os == "Macos":
                self.cpp_info.includedirs.extend(["include/compat/osx"])
            else:
                self.cpp_info.includedirs.extend(["include/compat/ios"])

        self.env_info.CMAKE_PREFIX_PATH.append(
            os.path.join(self.package_folder, "lib64", "cmake")
        )

    def deploy(self):
        self.copy("*", symlinks=True)
