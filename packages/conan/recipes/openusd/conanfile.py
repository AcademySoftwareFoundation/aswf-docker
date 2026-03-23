# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/EstebanDugueperoux2/conan-center-index/blob/1d8986d11305e1303b1581532f327cdd9d32ed20/recipes/openusd/all/conanfile.py

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.apple import is_apple_os
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, get, rm, rmdir
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv
from conan.tools.scm import Version

import os

required_conan_version = ">=1.53.0"

class OpenUSDConan(ConanFile):
    name = "openusd"
    description = "Universal Scene Description"
    license = "DocumentRef-LICENSE.txt:LicenseRef-Modified-Apache-2.0-License"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://openusd.org/"
    topics = ("3d", "scene", "usd")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_alembic": [True, False],     # ASWF: build with Alembic plugin
        "with_hdf5": [True, False],        # ASWF: build with HDF5 for Alembic
        "with_gpu": [True, False],         # ASWF: build with GPU support
        "with_gl":  [True, False],         # ASWF: build with OpenGL
        "with_metal": [True, False],       # ASWF: build with Metal
        "with_vulkan": [True, False],      # ASWF: build with Vulkan
        "with_materialx": [True, False],   # ASWF: build with MaterialX
        "with_opencolorio": [True, False], # ASWF: build OpenColorIO plugin
        "with_openimageio": [True, False], # ASWF: build OpenImageIO plugin
        "with_openvdb": [True, False],     # ASWF: build with OpenVDB
        "with_osl": [True, False],         # ASWF: build with OpenShadingLanguage
        "with_ptex": [True, False],        # ASWF: build with Ptex
        "with_python": [True, False],      # ASWF: build with Python
        "with_usdview": [True, False],     # ASWF: build usdview
    }
    default_options = {
        "shared": False,
        "fPIC": False,
        "with_alembic": True ,     # ASWF: build with Alembic plugin
        "with_hdf5": True,         # ASWF: build with HDF5 for Alembic
        "with_gpu": True,          # ASWF: build with GPU support
        "with_gl": True,           # ASWF: build with OpenGL
        "with_metal": False,       # ASWF: build with Metal
        "with_vulkan": False,      # ASWF: build with Vulkan, requires VULKAN_SDK and libshaderc
        "with_materialx": True,    # ASWF: build with MateriaX
        "with_opencolorio": True,  # ASWF: build OpenColorIO plugin
        "with_openimageio": True,  # ASWF: build OpenImageIO plugin
        "with_openvdb": True,      # ASWF: build with OpenVDB
        "with_osl": True,          # ASWF: build with OpenShadingLanguage
        "with_ptex": True,         # ASWF: build with Ptex
        "with_python": True,       # ASWF: build with Python
        "with_usdview": True,      # ASWF: build usdview
    }

    short_paths = True

    @property
    def _min_cppstd(self):
        return 17

    @property
    def _compilers_minimum_version(self):
        # as defined in https://github.com/PixarAnimationStudios/OpenUSD/blob/release/VERSIONS.md
        return {
            "apple-clang": "13",
            "clang": "7",
            "gcc": "9",
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

    def requirements(self):
        self.requires("onetbb/2021.12.0", transitive_headers=True, transitive_libs=True)
        self.requires("opensubdiv/3.7.0")
        self.requires("opengl/system")
        # ASWF: optional requirements
        if self.options.with_alembic:
            self.requires("alembic/1.8.10")
        if self.options.with_hdf5:
            self.requires("hdf5/1.14.6")
        if self.options.with_materialx:
            self.requires("materialx/1.39.4")
        if self.options.with_opencolorio:
            self.requires("ocio/2.5.1")
        if self.options.with_openimageio:
            self.requires("oiio/3.1.10.0")
        if self.options.with_openvdb:
            self.requires("openvdb/13.0.0")
        if self.options.with_osl:
            self.requires("osl/1.15.1.0")
        if self.options.with_ptex:
            self.requires("ptex/2.4.3")
        if self.options.with_python:
            self.requires("cpython/[>=3.9]", transitive_headers=True, transitive_libs=True)
            if Version(self.version) < "25.05":
                self.requires("boost/1.84.0", transitive_headers=True, transitive_libs=True)
        if self.options.with_usdview:
            self.requires("pyside/6.8.3") 

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.16 <4]")
        self.tool_requires("cpython/[>=3.0.0]")
        if self.options.with_usdview:
            # ASWF: building usdview requires running uic tool from pyside
            self.tool_requires("pyside/6.8.3")

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, self._min_cppstd)
        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if minimum_version and Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(
                f"{self.ref} requires C++{self._min_cppstd}, which your compiler does not support."
            )
        # Require same options as in https://github.com/PixarAnimationStudios/OpenUSD/blob/release/build_scripts/build_usd.py#L1450
        if not self.dependencies["opensubdiv"].options.with_tbb and self.options.shared:
            raise ConanInvalidConfiguration("openusd requires -o opensubdiv/*:with_tbb=True when building shared")
        if not self.dependencies["opensubdiv"].options.with_opengl:
            raise ConanInvalidConfiguration("openusd requires -o opensubdiv/*:with_opengl=True")
        # As onetbb is a hard requirement if OpenUSD and onetbb forbids static build then we cannot support static builds
        # See https://github.com/conan-io/conan/issues/15040#issuecomment-1790753531
        if not self.options.shared:
            raise ConanInvalidConfiguration("openusd does not supports static build because onetbb conancenter recipe forbids it")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        # Use variables in documented in https://github.com/PixarAnimationStudios/OpenUSD/blob/release/BUILDING.md
        tc.variables["PXR_BUILD_USDVIEW"] = self.options.with_usdview # ASWF: build usdview
        if self.options.with_usdview:
            # ASWF: USD needs to be told where uic lives
            pyside_info = self.dependencies["pyside"]
            tc.variables["PYSIDEUICBINARY"] = os.path.join(
                pyside_info.package_folder,
                pyside_info.cpp_info.bindirs[0],
                "uic"
            )

        tc.variables["PXR_BUILD_TESTS"] = False
        tc.variables["PXR_BUILD_EXAMPLES"] = False
        tc.variables["PXR_BUILD_TUTORIALS"] = False
        tc.variables["PXR_BUILD_HTML_DOCUMENTATION"] = False
        tc.variables["PXR_BUILD_ALEMBIC_PLUGIN"] = self.options.with_alembic       # ASWF: build Alembic plugin
        tc.variables["PXR_ENABLE_HDF5_SUPPORT"] = self.options.with_hdf5           # ASWF: build HDF5 for Alembic
        tc.variables["PXR_BUILD_GPU_SUPPORT"] = self.options.with_gpu              # ASWF: build GPU support
        tc.variables["PXR_ENABLE_GL_SUPPORT"] = self.options.with_gl               # ASWF: build OpenGL
        tc.variables["PXR_ENABLE_METAL_SUPPORT"] = self.options.with_metal         # ASWF: build Metal
        tc.variables["PXR_ENABLE_VULKAN_SUPPORT"] = self.options.with_vulkan       # ASWF: build Vulkan

        tc.variables["PXR_ENABLE_MATERIALX_SUPPORT"] = self.options.with_materialx   # ASWF: build MaterialX support
        if self.options.with_materialx:
            materialx_info = self.dependencies["materialx"]
            tc.variables["MATERIALX_STDLIB_DIR"] = os.path.join(materialx_info.package_folder,"share","MaterialX")
        tc.variables["PXR_BUILD_OPENCOLORIO_PLUGIN"] = self.options.with_opencolorio # ASWF: build OpenColorIO plugin
        tc.variables["PXR_BUILD_OPENIMAGEIO_PLUGIN"] = self.options.with_openimageio # ASWF: build OpenImageIO plugin
        tc.variables["PXR_ENABLE_OPENVDB_SUPPORT"] = self.options.with_openvdb       # ASWF: build OpenVDB support
        tc.variables["PXR_ENABLE_OSL_SUPPORT"] = self.options.with_osl               # ASWF: build OpenShadingLanguage components
        tc.variables["PXR_ENABLE_PTEX_SUPPORT"] = self.options.with_ptex             # ASWF: build Ptex support
        tc.variables["PXR_ENABLE_PYTHON_SUPPORT"] = self.options.with_python         # ASWF: build Python support
       
        tc.variables["OPENSUBDIV_LIBRARIES"] = "OpenSubdiv::osdcpu;OpenSubdiv::osdgpu"
        tc.variables["OPENSUBDIV_INCLUDE_DIR"] = self.dependencies['opensubdiv'].cpp_info.includedirs[0].replace("\\", "/")
        target_suffix = "" if self.dependencies["opensubdiv"].options.shared else "_static"
        tc.variables["OPENSUBDIV_OSDCPU_LIBRARY"] = "OpenSubdiv::osdcpu"+target_suffix
        tc.variables["TBB_tbb_LIBRARY"] = "TBB::tbb"
        tc.generate()

        tc = CMakeDeps(self)
        tc.set_property("opensubdiv::osdcpu", "cmake_target_name", "OpenSubdiv::osdcpu")
        tc.set_property("opensubdiv::osdcpu", "cmake_target_aliases", ["OpenSubdiv::osdcpu_static"])

        tc.generate()

    def build(self):
        # ASWF: apply patches
        apply_conandata_patches(self)

        if self.options.with_python:
            # ASWF: USD requires some Python modules
            import subprocess
            python_info = self.dependencies["cpython"]
            python_bin = os.path.join(
                python_info.package_folder,
                python_info.cpp_info.bindirs[0],
                "python"
            )
            subprocess.check_call([python_bin, "-m", "pip", "install", "PyOpenGL", "jinja2"])
 
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # ASWF: license files in package subdirectory
        copy(self, "LICENSE.txt", self.source_folder, os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()

        # ASWF: keep cmake for outside conan use
        # rm(self, "pxrConfig.cmake", self.package_folder)
        # rmdir(self, os.path.join(self.package_folder, "cmake"))

    def package_info(self):
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("m")
            self.cpp_info.system_libs.append("pthread")
            self.cpp_info.system_libs.append("dl")
  
        self.cpp_info.components["usd_arch"].libs = ["usd_arch"]

        self.cpp_info.components["usd_ar"].libs = ["usd_ar"]
        self.cpp_info.components["usd_ar"].requires = ["usd_arch", "usd_js", "usd_tf", "usd_plug", "usd_vt"]
        if self.options.shared:
            self.cpp_info.components["usd_ar"].requires.append("onetbb::libtbb")

        self.cpp_info.components["usd_cameraUtil"].libs = ["usd_cameraUtil"]
        self.cpp_info.components["usd_cameraUtil"].requires = ["usd_tf", "usd_gf"]

        self.cpp_info.components["usd_garch"].libs = ["usd_garch"]
        self.cpp_info.components["usd_garch"].requires = ["usd_arch", "usd_tf", "opengl::opengl"]
    
        self.cpp_info.components["usd_geomUtil"].libs = ["usd_geomUtil"]
        self.cpp_info.components["usd_geomUtil"].requires = ["usd_arch", "usd_gf", "usd_tf", "usd_vt", "usd_pxOsd"]

        self.cpp_info.components["usd_gf"].libs = ["usd_gf"]
        self.cpp_info.components["usd_gf"].requires = ["usd_arch", "usd_tf"]

        self.cpp_info.components["usd_glf"].libs = ["usd_glf"]
        self.cpp_info.components["usd_glf"].requires = ["usd_ar", "usd_arch", "usd_garch", "usd_gf", "usd_hf", "usd_hio", "usd_plug", "usd_tf", "usd_trace", "usd_sdf", "opengl::opengl"]

        self.cpp_info.components["usd_hd"].libs = ["usd_hd"]
        self.cpp_info.components["usd_hd"].requires = ["usd_plug", "usd_tf", "usd_trace", "usd_vt", "usd_work", "usd_sdf", "usd_cameraUtil", "usd_hf", "usd_pxOsd", "usd_sdr"]
        if self.options.shared:
            self.cpp_info.components["usd_hd"].requires.append("onetbb::libtbb")

        self.cpp_info.components["usd_hdar"].libs = ["usd_hdar"]
        self.cpp_info.components["usd_hdar"].requires = ["usd_hd", "usd_ar"]

        self.cpp_info.components["usd_hdGp"].libs = ["usd_hdGp"]
        self.cpp_info.components["usd_hdGp"].requires = ["usd_hd", "usd_hf"]
        if self.options.shared:
            self.cpp_info.components["usd_hdGp"].requires.append("onetbb::libtbb")

        self.cpp_info.components["usd_hdsi"].libs = ["usd_hdsi"]
        self.cpp_info.components["usd_hdsi"].requires = ["usd_plug", "usd_tf", "usd_trace", "usd_vt", "usd_work", "usd_sdf", "usd_cameraUtil", "usd_geomUtil", "usd_hf", "usd_hd", "usd_pxOsd"]

        self.cpp_info.components["usd_hdSt"].libs = ["usd_hdSt"]
        self.cpp_info.components["usd_hdSt"].requires = ["usd_hio", "usd_garch", "usd_glf", "usd_hd", "usd_hdsi", "usd_hgiGL", "usd_hgiInterop", "usd_sdr", "usd_tf", "usd_trace", "opensubdiv::opensubdiv"]
        if self.options.with_ptex:
            self.cpp_info.components["usd_hdSt"].requires.append("ptex::ptex")
        if self.options.with_materialx:
            self.cpp_info.components["usd_hdSt"].requires.extend(["materialx::MaterialXCore", "materialx::MaterialXFormat", "materialx::MaterialXGenShader",
                                                                  "materialx::MaterialXGenGlsl", "materialx::MaterialXGenMsl", "materialx::MaterialXRender"])
        if self.options.with_openimageio:
            self.cpp_info.components["usd_hdSt"].requires.append("oiio::OpenImageIO")

        self.cpp_info.components["usd_hdx"].libs = ["usd_hdx"]
        self.cpp_info.components["usd_hdx"].requires = ["usd_plug", "usd_tf", "usd_vt", "usd_gf", "usd_work", "usd_garch", "usd_glf", "usd_pxOsd", "usd_hd", "usd_hdSt", "usd_hgi", "usd_hgiInterop", "usd_cameraUtil", "usd_sdf"]
        if self.options.with_ptex:
            self.cpp_info.components["usd_hdx"].requires.append("ptex::ptex")
        if self.options.with_materialx:
            self.cpp_info.components["usd_hdx"].requires.extend(["materialx::MaterialXCore", "materialx::MaterialXFormat", "materialx::MaterialXGenShader",
                                                                 "materialx::MaterialXGenGlsl", "materialx::MaterialXGenMsl", "materialx::MaterialXRender"])
        if self.options.with_opencolorio:
            self.cpp_info.components["usd_hdx"].requires.append("ocio::ocio")
        if self.options.with_openimageio:
            self.cpp_info.components["usd_hdx"].requires.append("oiio::OpenImageIO")

        self.cpp_info.components["usd_hf"].libs = ["usd_hf"]
        self.cpp_info.components["usd_hf"].requires = ["usd_plug", "usd_tf", "usd_trace"]

        self.cpp_info.components["usd_hgi"].libs = ["usd_hgi"]
        self.cpp_info.components["usd_hgi"].requires = ["usd_gf", "usd_plug", "usd_tf", "usd_hio"]

        self.cpp_info.components["usd_hgiGL"].libs = ["usd_hgiGL"]
        self.cpp_info.components["usd_hgiGL"].requires = ["usd_arch", "usd_garch", "usd_hgi", "usd_tf", "usd_trace"]

        if is_apple_os(self):
            self.cpp_info.components["usd_hgiMetal"].libs = ["usd_hgiMetal"]
            self.cpp_info.components["usd_hgiMetal"].requires = ["usd_arch", "usd_hgi", "usd_tf", "usd_trace"]

        self.cpp_info.components["usd_hgiInterop"].libs = ["usd_hgiInterop"]
        self.cpp_info.components["usd_hgiInterop"].requires = ["usd_garch", "usd_gf", "usd_tf", "usd_hgi", "usd_vt", "usd_trace"]
        if is_apple_os(self):
            self.cpp_info.components["usd_hgiInterop"].requires.append("usd_hgiMetal")

        self.cpp_info.components["usd_hio"].libs = ["usd_hio"]
        self.cpp_info.components["usd_hio"].requires = ["usd_arch", "usd_js", "usd_plug", "usd_tf", "usd_vt", "usd_trace", "usd_ar", "usd_hf"]

        self.cpp_info.components["usd_js"].libs = ["usd_js"]
        self.cpp_info.components["usd_js"].requires = ["usd_tf"]

        self.cpp_info.components["usd_kind"].libs = ["usd_kind"]
        self.cpp_info.components["usd_kind"].requires = ["usd_tf", "usd_plug"]

        self.cpp_info.components["usd_pcp"].libs = ["usd_pcp"]
        self.cpp_info.components["usd_pcp"].requires = ["usd_tf", "usd_trace", "usd_vt", "usd_sdf", "usd_work", "usd_ar"]
        if self.options.shared:
            self.cpp_info.components["usd_pcp"].requires.append("onetbb::libtbb")

        self.cpp_info.components["usd_pegtl"].libs = ["usd_pegtl"]
        self.cpp_info.components["usd_pegtl"].requires = ["usd_arch"]

        self.cpp_info.components["usd_plug"].libs = ["usd_plug"]
        self.cpp_info.components["usd_plug"].requires = ["usd_arch", "usd_tf", "usd_js", "usd_trace", "usd_work"]
        if self.options.shared:
            self.cpp_info.components["usd_plug"].requires.append("onetbb::libtbb")

        self.cpp_info.components["usd_pxOsd"].libs = ["usd_pxOsd"]
        self.cpp_info.components["usd_pxOsd"].requires = ["usd_tf", "usd_gf", "usd_vt", "opensubdiv::opensubdiv"]

        self.cpp_info.components["usd_sdf"].libs = ["usd_sdf"]
        self.cpp_info.components["usd_sdf"].requires = ["usd_arch", "usd_tf", "usd_ts", "usd_gf", "usd_trace", "usd_vt", "usd_work", "usd_ar"]

        self.cpp_info.components["usd_sdr"].libs = ["usd_sdr"]
        self.cpp_info.components["usd_sdr"].requires = ["usd_tf", "usd_vt", "usd_ar", "usd_sdf"]

        self.cpp_info.components["usd_tf"].libs = ["usd_tf"]
        self.cpp_info.components["usd_tf"].requires = ["usd_arch"]
        if self.options.shared:
            self.cpp_info.components["usd_tf"].requires.append("onetbb::libtbb")
        # ASWF: if building against Python is requested, almost every DSO is linked
        # against libusd_python.so and Python includes are required throughout.
        # Since almost every component requires usd_tf, we add the dependency here.
        # Transition from boost::python to usd_python in USD 25.05
        if self.options.with_python:
            if Version(self.version) < "25.05":
                self.cpp_info.components["usd_tf"].requires.append("boost::python")
            else:
                self.cpp_info.components["usd_boost"].libs = ["usd_boost"]
                self.cpp_info.components["usd_tf"].requires.append("usd_python")
                self.cpp_info.components["usd_python"].libs = ["usd_python"]
                self.cpp_info.components["usd_python"].requires = ["usd_boost", "cpython::cpython"]

        self.cpp_info.components["usd_trace"].libs = ["usd_trace"]
        self.cpp_info.components["usd_trace"].requires = ["usd_arch", "usd_tf", "usd_js"]
        if self.options.shared:
            self.cpp_info.components["usd_trace"].requires.append("onetbb::libtbb")

        self.cpp_info.components["usd_ts"].libs = ["usd_ts"]
        self.cpp_info.components["usd_ts"].requires = ["usd_arch", "usd_gf", "usd_plug", "usd_tf", "usd_trace", "usd_vt"]

        self.cpp_info.components["usd_usd"].libs = ["usd_usd"]
        self.cpp_info.components["usd_usd"].requires = ["usd_arch", "usd_kind", "usd_pcp", "usd_sdf", "usd_ar", "usd_plug", "usd_tf", "usd_trace", "usd_vt", "usd_work"]
        if self.options.shared:
            self.cpp_info.components["usd_usd"].requires.append("onetbb::libtbb")

        self.cpp_info.components["usd_usdAppUtils"].libs = ["usd_usdAppUtils"]
        self.cpp_info.components["usd_usdAppUtils"].requires = ["usd_garch", "usd_gf", "usd_hio", "usd_sdf", "usd_tf", "usd_usd", "usd_usdGeom", "usd_usdImagingGL"]
        if self.options.with_ptex:
            self.cpp_info.components["usd_usdAppUtils"].requires.append("ptex::ptex")
        if self.options.with_materialx:
            self.cpp_info.components["usd_usdAppUtils"].requires.extend(["materialx::MaterialXCore", "materialx::MaterialXFormat",
                                                                         "materialx::MaterialXGenShader", "materialx::MaterialXRender",
                                                                         "materialx::MaterialXGenGlsl", "materialx::MaterialXGenMsl"])
        if self.options.with_opencolorio:
            self.cpp_info.components["usd_usdAppUtils"].requires.append("ocio::ocio")
        if self.options.with_openimageio:
            self.cpp_info.components["usd_usdAppUtils"].requires.append("oiio::OpenImageIO")                                                              

        self.cpp_info.components["usd_usdGeom"].libs = ["usd_usdGeom"]
        self.cpp_info.components["usd_usdGeom"].requires = ["usd_js", "usd_tf", "usd_plug", "usd_vt", "usd_sdf", "usd_trace", "usd_usd", "usd_work"]
        if self.options.shared:
            self.cpp_info.components["usd_usdGeom"].requires.append("onetbb::libtbb")

        if Version(self.version) >= "25.02":
            self.cpp_info.components["usd_usdGeomValidators"].libs = ["usd_usdGeomValidators"]
            self.cpp_info.components["usd_usdGeomValidators"].requires = ["usd_tf", "usd_plug", "usd_sdf", "usd_usd", "usd_usdGeom", "usd_usdValidation"]
        
        self.cpp_info.components["usd_usdHydra"].libs = ["usd_usdHydra"]
        self.cpp_info.components["usd_usdHydra"].requires = ["usd_tf", "usd_usd", "usd_usdShade"]

        self.cpp_info.components["usd_usdImaging"].libs = ["usd_usdImaging"]
        self.cpp_info.components["usd_usdImaging"].requires = ["usd_gf", "usd_tf", "usd_plug", "usd_trace", "usd_vt", "usd_work", "usd_geomUtil", "usd_hd", "usd_hdar", "usd_hio", "usd_pxOsd", "usd_sdf", "usd_usd", "usd_usdGeom", "usd_usdLux", "usd_usdRender", "usd_usdShade", "usd_usdVol", "usd_ar"]
        if self.options.shared:
            self.cpp_info.components["usd_usdImaging"].requires.append("onetbb::libtbb")

        self.cpp_info.components["usd_usdImagingGL"].libs = ["usd_usdImagingGL"]
        self.cpp_info.components["usd_usdImagingGL"].requires = ["usd_gf", "usd_tf", "usd_plug", "usd_trace", "usd_vt", "usd_work", "usd_hio", "usd_garch", "usd_glf", "usd_hd", "usd_hdsi", "usd_hdx", "usd_pxOsd", "usd_sdf", "usd_sdr", "usd_usd", "usd_usdGeom", "usd_usdHydra", "usd_usdShade", "usd_usdImaging", "usd_ar"]
        if self.options.shared:
            self.cpp_info.components["usd_usdImagingGL"].requires.append("onetbb::libtbb")
        if self.options.with_ptex:
            self.cpp_info.components["usd_usdImagingGL"].requires.append("ptex::ptex")
        if self.options.with_materialx:
            self.cpp_info.components["usd_usdImagingGL"].requires.extend(["materialx::MaterialXCore", "materialx::MaterialXFormat",
                                                                          "materialx::MaterialXGenShader", "materialx::MaterialXRender",
                                                                          "materialx::MaterialXGenGlsl", "materialx::MaterialXGenMsl"])
        if self.options.with_opencolorio:
            self.cpp_info.components["usd_usdImagingGL"].requires.append("ocio::ocio")
        if self.options.with_openimageio:
            self.cpp_info.components["usd_usdImagingGL"].requires.append("oiio::OpenImageIO")

        self.cpp_info.components["usd_usdLux"].libs = ["usd_usdLux"]
        self.cpp_info.components["usd_usdLux"].requires = ["usd_tf", "usd_vt", "usd_sdf", "usd_usd", "usd_usdGeom", "usd_usdShade"]

        self.cpp_info.components["usd_usdMedia"].libs = ["usd_usdMedia"]
        self.cpp_info.components["usd_usdMedia"].requires = ["usd_tf", "usd_vt", "usd_sdf", "usd_usd", "usd_usdGeom"]

        self.cpp_info.components["usd_usdPhysics"].libs = ["usd_usdPhysics"]
        self.cpp_info.components["usd_usdPhysics"].requires = ["usd_tf", "usd_plug", "usd_vt", "usd_sdf", "usd_trace", "usd_usd", "usd_usdGeom", "usd_usdShade", "usd_work"]
        if self.options.shared:
            self.cpp_info.components["usd_usdPhysics"].requires.append("onetbb::libtbb")
        
        if Version(self.version) >= "25.02":
            self.cpp_info.components["usd_usdPhysicsValidators"].libs = ["usd_usdPhysicsValidators"]

        self.cpp_info.components["usd_usdProc"].libs = ["usd_usdProc"]
        self.cpp_info.components["usd_usdProc"].requires = ["usd_tf", "usd_usd", "usd_usdGeom"]

        self.cpp_info.components["usd_usdProcImaging"].libs = ["usd_usdProcImaging"]
        self.cpp_info.components["usd_usdProcImaging"].requires = ["usd_usdImaging", "usd_usdProc"]

        self.cpp_info.components["usd_usdRender"].libs = ["usd_usdRender"]
        self.cpp_info.components["usd_usdRender"].requires = ["usd_gf", "usd_tf", "usd_usd", "usd_usdGeom", "usd_usdShade"]

        self.cpp_info.components["usd_usdRi"].libs = ["usd_usdRi"]
        self.cpp_info.components["usd_usdRi"].requires = ["usd_tf", "usd_vt", "usd_sdf", "usd_usd", "usd_usdShade", "usd_usdGeom"]

        self.cpp_info.components["usd_usdRiPxrImaging"].libs = ["usd_usdRiPxrImaging"]
        self.cpp_info.components["usd_usdRiPxrImaging"].requires = ["usd_gf", "usd_tf", "usd_plug", "usd_trace", "usd_vt", "usd_work", "usd_hd", "usd_pxOsd", "usd_sdf", "usd_usd", "usd_usdGeom", "usd_usdLux", "usd_usdShade", "usd_usdImaging", "usd_usdVol", "usd_ar"]
        if self.options.shared:
            self.cpp_info.components["usd_usdRiPxrImaging"].requires.append("onetbb::libtbb")

        if Version(self.version) > "24.08":
            self.cpp_info.components["usd_usdSemantics"].libs = ["usd_usdSemantics"]
        
        self.cpp_info.components["usd_usdShade"].libs = ["usd_usdShade"]
        self.cpp_info.components["usd_usdShade"].requires = ["usd_tf", "usd_vt", "usd_js", "usd_sdf", "usd_sdr", "usd_usd", "usd_usdGeom"]
        
        if Version(self.version) >= "25.02":
            self.cpp_info.components["usd_usdShadeValidators"].libs = ["usd_usdShadeValidators"]

        self.cpp_info.components["usd_usdSkel"].libs = ["usd_usdSkel"]
        self.cpp_info.components["usd_usdSkel"].requires = ["usd_arch", "usd_gf", "usd_tf", "usd_trace", "usd_vt", "usd_work", "usd_sdf", "usd_usd", "usd_usdGeom"]
        if self.options.shared:
            self.cpp_info.components["usd_usdSkel"].requires.append("onetbb::libtbb")

        self.cpp_info.components["usd_usdSkelImaging"].libs = ["usd_usdSkelImaging"]
        self.cpp_info.components["usd_usdSkelImaging"].requires = ["usd_hio", "usd_hd", "usd_usdImaging", "usd_usdSkel"]

        if Version(self.version) >= "25.02":
            self.cpp_info.components["usd_usdSkelValidators"].libs = ["usd_usdSkelValidators"]

        self.cpp_info.components["usd_usdUI"].libs = ["usd_usdUI"]
        self.cpp_info.components["usd_usdUI"].requires = ["usd_tf", "usd_vt", "usd_sdf", "usd_usd"]

        self.cpp_info.components["usd_usdUtils"].libs = ["usd_usdUtils"]
        self.cpp_info.components["usd_usdUtils"].requires = ["usd_arch", "usd_tf", "usd_gf", "usd_sdf", "usd_usd", "usd_usdGeom", "usd_usdShade"]
        
        if Version(self.version) >= "25.02":
            self.cpp_info.components["usd_usdUtilsValidators"].libs = ["usd_usdUtilsValidators"]
            self.cpp_info.components["usd_usdValidation"].libs = ["usd_usdValidation"]

        self.cpp_info.components["usd_usdVol"].libs = ["usd_usdVol"]
        self.cpp_info.components["usd_usdVol"].requires = ["usd_tf", "usd_usd", "usd_usdGeom"]

        self.cpp_info.components["usd_usdVolImaging"].libs = ["usd_usdVolImaging"]
        self.cpp_info.components["usd_usdVolImaging"].requires = ["usd_usdImaging"]
        
        self.cpp_info.components["usd_vt"].libs = ["usd_vt"]
        self.cpp_info.components["usd_vt"].requires = ["usd_arch", "usd_tf", "usd_gf", "usd_trace"]
        if self.options.shared:
            self.cpp_info.components["usd_vt"].requires.append("onetbb::libtbb")
            
        self.cpp_info.components["usd_work"].libs = ["usd_work"]
        self.cpp_info.components["usd_work"].requires = ["usd_tf", "usd_trace"]
        if self.options.shared:
            self.cpp_info.components["usd_work"].requires.append("onetbb::libtbb")

        # ASWF: components and requirements for additional components
        if self.options.with_alembic:
            self.cpp_info.components["usd_usdAbc"].requires = ["alembic::alembic"]
            if self.options.with_hdf5:
                self.cpp_info.components["usd_usdAbc"].requires.append("hdf5::hdf5")
            if self.options.shared:
                self.cpp_info.components["usd_usdAbc"].requires.append("onetbb::libtbb")
            self.cpp_info.components["usd_usdAbc"].bindirs = [ os.path.join("plugins", "usd") ]

        if self.options.with_materialx:
            self.cpp_info.components["usd_usdMtlx"].libs = ["usd_usdMtlx"]
            self.cpp_info.components["usd_usdMtlx"].requires = ["materialx::MaterialXCore", "materialx::MaterialXFormat"]
            self.cpp_info.components["usd_usdBakeMtlx"].libs = ["usd_usdBakeMtlx"]
            self.cpp_info.components["usd_usdBakeMtlx"].requires = ["materialx::MaterialXCore", "materialx::MaterialXFormat",
                                                                    "materialx::MaterialXRenderGlsl", "materialx::MaterialXRenderHw",
                                                                    "materialx::MaterialXGenGlsl", "materialx::MaterialXRender",
                                                                    "materialx::MaterialXGenShader"]

            if self.options.shared:
                self.cpp_info.components["usd_usdMtlx"].requires.append("onetbb::libtbb")
                self.cpp_info.components["usd_usdBakeMtlx"].requires.append("onetbb::libtbb")
            if self.options.with_openimageio:
                    self.cpp_info.components["usd_usdBakeMtlx"].requires.append("oiio::OpenImageIO")

        if self.options.with_openvdb:
            self.cpp_info.components["usd_usdHioOpenVDB"].requires = ["openvdb::openvdb"]

        if self.options.with_osl:
            self.cpp_info.components["usd_usdOsl"].requires = ["osl::osl"]
            self.cpp_info.components["usd_usdOsl"].bindirs = [ os.path.join("plugins", "usd") ]

        if self.options.with_usdview: 
            self.cpp_info.components["usd_usdview"].requires = ["cpython::cpython", "pyside::pyside"]
            if self.options.shared:
                self.cpp_info.components["usd_usdview"].requires.append("onetbb::libtbb")

