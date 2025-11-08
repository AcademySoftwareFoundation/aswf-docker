# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/openimageio/all/conanfile.py

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, get, rm, rmdir
from conan.tools.microsoft import is_msvc, is_msvc_static_runtime
from conan.tools.scm import Version
from conan.errors import ConanInvalidConfiguration
import os

required_conan_version = ">=1.53.0"


class OpenImageIOConan(ConanFile):
    name = "oiio" # ASWF: short name for compatibility
    description = (
        "OpenImageIO is a library for reading and writing images, and a bunch "
        "of related classes, utilities, and applications. There is a "
        "particular emphasis on formats and functionality used in "
        "professional, large-scale animation and visual effects work for film."
    )
    topics = ("vfx", "image", "picture")
    license = "Apache-2.0", "BSD-3-Clause"
    homepage = "http://www.openimageio.org/"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_libjpeg": ["libjpeg", "libjpeg-turbo"],
        "with_libpng": [True, False],
        "with_freetype": [True, False],
        "with_hdf5": [True, False],
        "with_opencolorio": [True, False],
        "with_opencv": [True, False],
        "with_tbb": [True, False],
        "with_dicom": [True, False],
        "with_ffmpeg": [True, False],
        "with_giflib": [True, False],
        "with_libheif": [True, False],
        "with_raw": [True, False],
        "with_openjpeg": [True, False],
        "with_openvdb": [True, False],
        "with_ptex": [True, False],
        "with_libwebp": [True, False],
        "with_libjxl": [True, False],
        "with_libultrahdr": [True, False],
        "with_iv": [True, False],
        "with_python": [True, False], # ASWF
        "with_openjph": [True, False], # ASWF
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_libjpeg": "libjpeg-turbo", # ASWF: EL distros default to -turbo
        "with_libpng": True,
        "with_freetype": True,
        "with_hdf5": True,
        "with_opencolorio": True,
        "with_opencv": False,
        "with_tbb": True, # ASWF: exercise dependency
        "with_dicom": False,  # Heavy dependency, disabled by default
        "with_ffmpeg": False, # ASWF: disable until we resolve dependencies
        "with_giflib": True,
        "with_libheif": False,# ASWF: disable until we resolve dependencies
        "with_raw": True,  # libraw is available under CDDL-1.0 or LGPL-2.1, for this reason it is disabled by default ASWF: enable for rawtoaces
        "with_openjpeg": True,
        "with_openvdb": False,  # FIXME: broken on M1
        "with_ptex": True,
        "with_libwebp": True,
        "with_libjxl": True,
        "with_libultrahdr": True,
        "with_iv": False, # ASWF: enable once we figure out why configure doesn't find Qt or OpenGL
        "with_python": True, # ASWF: build Python bindings
        "with_openjph": True, # ASWF: use OpenJPH since OpenEXR uses it
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
        # Required libraries
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires("boost/1.84.0")
        self.requires("libtiff/4.6.0")
        self.requires("imath/3.1.9", transitive_headers=True)
        self.requires("openexr/3.2.3")
        if self.options.with_libjpeg == "libjpeg":
            self.requires("libjpeg/9e")
        elif self.options.with_libjpeg == "libjpeg-turbo":
            self.requires("libjpeg-turbo/3.0.2")
        self.requires("pugixml/1.14")
        self.requires("libsquish/1.15")
        self.requires("tsl-robin-map/1.2.1")
        if Version(self.version) >= "2.4.17.0":
            self.requires("fmt/10.2.1", transitive_headers=True)
        else:
            self.requires("fmt/9.1.0", transitive_headers=True)
        self.requires("pybind11/[>=2.0.0]") # ASWF: OIIO now uses pybind11

        # Optional libraries
        if self.options.with_libpng:
            self.requires("libpng/[>=1.6 <2]")
        if self.options.with_freetype:
            self.requires("freetype/2.13.2")
        if self.options.with_hdf5:
            self.requires("hdf5/1.14.3")
        if self.options.with_opencolorio:
            self.requires("ocio/2.3.1")  # ASWF: ocio for backwards compatibility
        if self.options.with_opencv:
            self.requires("opencv/4.8.1")
        if self.options.with_tbb:
            self.requires("onetbb/2021.10.0")
        if self.options.with_dicom:
            self.requires("dcmtk/3.6.7")
        if self.options.with_ffmpeg:
            self.requires("ffmpeg/6.1")
        # TODO: Field3D dependency
        if self.options.with_giflib:
            self.requires("giflib/5.2.1")
        if self.options.with_libheif:
            self.requires("libheif/1.16.2")
        if self.options.with_raw:
            self.requires("libraw/0.21.2")
        if self.options.with_openjpeg:
            self.requires("openjpeg/2.5.2")
        if self.options.with_openvdb:
            self.requires("openvdb/8.0.1")
        if self.options.with_ptex:
            self.requires("ptex/2.4.2")
        if self.options.with_libwebp:
            self.requires("libwebp/1.3.2")
        if self.options.with_libjxl:
            self.requires("libjxl/0.11.1")
        if self.options.with_libultrahdr:
            self.requires("libultrahdr/1.4.0")
        # TODO: R3DSDK dependency
        # TODO: Nuke dependency
        if self.options.with_iv:
           self.requires("opengl/system")
           self.requires("qt/6.8.3")
        if self.options.with_python: # ASWF: build Python bindings
           self.requires("cpython/[>=3.0.0")
        if self.options.with_openjph: # ASWF: use OpenJPH for JPEG-2000
           self.requires("openjph/0.24.5")

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, 14)
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
        tc.variables["CMAKE_DEBUG_POSTFIX"] = ""  # Needed for 2.3.x.x+ versions
        tc.variables["OIIO_BUILD_TOOLS"] = True
        tc.variables["OIIO_BUILD_TESTS"] = False
        tc.variables["BUILD_DOCS"] = False
        tc.variables["INSTALL_DOCS"] = False
        tc.variables["INSTALL_FONTS"] = False
        tc.variables["INSTALL_CMAKE_HELPER"] = False
        tc.variables["EMBEDPLUGINS"] = True
        tc.variables["USE_PYTHON"] = True # ASWF: build Python bindings
        tc.variables["USE_EXTERNAL_PUGIXML"] = True
        tc.variables["BUILD_MISSING_FMT"] = False

        # Conan is normally not used for testing, so fixing this option to not build the tests
        tc.variables["BUILD_TESTING"] = False

        # OIIO CMake files are patched to check USE_* flags to require or not use dependencies
        tc.variables["USE_JPEGTURBO"] = (
            self.options.with_libjpeg == "libjpeg-turbo"
        )
        tc.variables[
            "USE_JPEG"
        ] = True  # Needed for jpeg.imageio plugin, libjpeg/libjpeg-turbo selection still works
        tc.variables["USE_HDF5"] = self.options.with_hdf5
        tc.variables["USE_OPENCOLORIO"] = self.options.with_opencolorio
        tc.variables["USE_OPENCV"] = self.options.with_opencv
        tc.variables["USE_TBB"] = self.options.with_tbb
        tc.variables["USE_DCMTK"] = self.options.with_dicom
        tc.variables["USE_FFMPEG"] = self.options.with_ffmpeg
        tc.variables["USE_FIELD3D"] = False
        tc.variables["USE_GIF"] = self.options.with_giflib
        tc.variables["USE_LIBHEIF"] = self.options.with_libheif
        tc.variables["USE_LIBRAW"] = self.options.with_raw
        tc.variables["USE_OPENVDB"] = self.options.with_openvdb
        tc.variables["USE_PTEX"] = self.options.with_ptex
        tc.variables["USE_R3DSDK"] = False
        tc.variables["USE_NUKE"] = False
        tc.variables["USE_OPENGL"] = False
        tc.variables["USE_QT"] = False
        tc.variables["USE_LIBPNG"] = self.options.with_libpng
        tc.variables["USE_FREETYPE"] = self.options.with_freetype
        tc.variables["USE_LIBWEBP"] = self.options.with_libwebp
        tc.variables["USE_OPENJPEG"] = self.options.with_openjpeg

        tc.generate()
        cd = CMakeDeps(self)
        cd.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
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
        return f"openimageio_{name.lower()}"

    def _add_component(self, name):
        component = self.cpp_info.components[self._conan_comp(name)]
        component.set_property("cmake_target_name", f"OpenImageIO::{name}")
        component.names["cmake_find_package"] = name
        component.names["cmake_find_package_multi"] = name
        return component

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenImageIO")
        self.cpp_info.set_property("cmake_target_name", "OpenImageIO::OpenImageIO") # ASWF: since we set name to oiio
        self.cpp_info.set_property("pkg_config_name", "OpenImageIO")

        self.cpp_info.names["cmake_find_package"] = "OpenImageIO"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenImageIO"

        # OpenImageIO::OpenImageIO_Util
        # ASWF: _add_component() deprecated in Conan 2.0
        self.cpp_info.components["OpenImageIO_Util"].libs = ["OpenImageIO_Util"]
        self.cpp_info.components["OpenImageIO_Util"].requires = [
            "boost::filesystem",
            "boost::thread",
            "boost::system",
            "boost::regex",
            "imath::imath",
            "openexr::openexr",
        ]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["OpenImageIO_Util"].system_libs.extend(
                ["dl", "m", "pthread"]
            )
        if self.options.with_tbb:
            self.cpp_info.components["OpenImageIO_Util"].requires.append("onetbb::onetbb")
        # ASWF: set correct CMake target name since our package is called oiio
        self.cpp_info.components["OpenImageIO_Util"].set_property("cmake_target_name", "OpenImageIO::OpenImageIO_Util")

        # OpenImageIO::OpenImageIO
        # ASWF: _add_component() deprecated in Conan 2.0
        self.cpp_info.components["OpenImageIO"].libs = ["OpenImageIO"]
        self.cpp_info.components["OpenImageIO"].requires = [
            "OpenImageIO_Util",
            "zlib::zlib",
            "boost::thread",
            "boost::system",
            "boost::container",
            "boost::regex",
            "libtiff::libtiff",
            "pugixml::pugixml",
            "tsl-robin-map::tsl-robin-map",
            "libsquish::libsquish",
            "fmt::fmt",
            "imath::imath",
            "openexr::openexr",
            "pybind11::pybind11",
        ]

        if self.options.with_libjpeg == "libjpeg":
            self.cpp_info.components["OpenImageIO"].requires.append("libjpeg::libjpeg")
        elif self.options.with_libjpeg == "libjpeg-turbo":
            self.cpp_info.components["OpenImageIO"].requires.append(
                "libjpeg-turbo::libjpeg-turbo"
            )
        if self.options.with_libpng:
            self.cpp_info.components["OpenImageIO"].requires.append("libpng::libpng")
        if self.options.with_freetype:
            self.cpp_info.components["OpenImageIO"].requires.append("freetype::freetype")
        if self.options.with_hdf5:
            self.cpp_info.components["OpenImageIO"].requires.append("hdf5::hdf5")
        if self.options.with_opencolorio:
            self.cpp_info.components["OpenImageIO"].requires.append("ocio::ocio") # ASWF: ocio instead of opencolorio for compat
        if self.options.with_opencv:
            self.cpp_info.components["OpenImageIO"].requires.append("opencv::opencv")
        if self.options.with_dicom:
            self.cpp_info.components["OpenImageIO"].requires.append("dcmtk::dcmtk")
        if self.options.with_ffmpeg:
            self.cpp_info.components["OpenImageIO"].requires.append("ffmpeg::ffmpeg")
        if self.options.with_giflib:
            self.cpp_info.components["OpenImageIO"].requires.append("giflib::giflib")
        if self.options.with_libheif:
            self.cpp_info.components["OpenImageIO"].requires.append("libheif::libheif")
        if self.options.with_raw:
            self.cpp_info.components["OpenImageIO"].requires.append("libraw::libraw")
        if self.options.with_openjpeg:
            self.cpp_info.components["OpenImageIO"].requires.append("openjpeg::openjpeg")
        if self.options.with_openvdb:
            self.cpp_info.components["OpenImageIO"].requires.append("openvdb::openvdb")
        if self.options.with_ptex:
            self.cpp_info.components["OpenImageIO"].requires.append("ptex::ptex")
        if self.options.with_libwebp:
            self.cpp_info.components["OpenImageIO"].requires.append("libwebp::libwebp")
        if self.options.with_libjxl: # ASWF: enable JPEG XL
            self.cpp_info.components["OpenImageIO"].requires.append("libjxl::libjxl")
        if self.options.with_libultrahdr: # ASWF: enable libultrahdr
            self.cpp_info.components["OpenImageIO"].requires.append("libultrahdr::libultrahdr")
        if self.options.with_python: # ASWF: build Python bindings
            self.cpp_info.components["OpenImageIO"].requires.append("cpython::cpython")
        if self.options.with_python: # ASWF: Use OpenJPH for JPEG-2000
            self.cpp_info.components["OpenImageIO"].requires.append("openjph::openjph")
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["OpenImageIO"].system_libs.extend(["dl", "m", "pthread"])

        if not self.options.shared:
            self.cpp_info.components["OpenImageIO"].defines.append("OIIO_STATIC_DEFINE")
