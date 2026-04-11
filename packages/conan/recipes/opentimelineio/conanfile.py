# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rmdir
from conan.tools.scm import Version
from conan.tools.env import Environment
import os

required_conan_version = ">=2"


class OpenTimelineIOConan(ConanFile):
    name = "opentimelineio"
    license = "Apache-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/AcademySoftwareFoundation/OpenTimelineIO"
    description = "Open Source API and interchange format for editorial timeline information."

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_pythonbind": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_pythonbind": False, # FIXME: disable python bindings until solution for
                                  # https://github.com/AcademySoftwareFoundation/OpenTimelineIO/issues/2007
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
        self.requires("cpython/[>=3.0.0]")
        self.tool_requires("cpython/[>=3.0.0]")
        if self.options.with_pythonbind:
            self.requires("pybind11/2.13.6")
        self.requires("imath/3.2.2", transitive_headers=True)
        self.requires("rapidjson/cci.20250205")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        # Dont use vendored copies
        tc.cache_variables["OTIO_CXX_INSTALL"] = True                            # Build and install C++ bindings
        tc.cache_variables["OTIO_PYTHON_INSTALL"] = self.options.with_pythonbind # Build and install Python bindings
        tc.cache_variables["OTIO_DEPENDENCIES_INSTALL"] = False              # Ignore vendored dependencies
        tc.cache_variables["OTIO_INSTALL_PYTHON_MODULES"] = True             # Install OTIO pure Python modules/files
        tc.cache_variables["OTIO_INSTALL_COMMANDLINE_TOOLS"] = True          # Install OTIO command line tools
        tc.cache_variables["OTIO_FIND_IMATH"] = True                         # Let CMake find Imath
        tc.cache_variables["OTIO_FIND_PYBIND11"] = True                      # Let CMake find pybind11
        tc.cache_variables["OTIO_FIND_RAPIDJSON"] = True                     # Let CMake find RapidJSON
        tc.cache_variables["OTIO_AUTOMATIC_SUBMODULES"] = False              # Don't refresh submodules
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # ASWF: separate license files per package
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenTimelineIO")
        self.cpp_info.set_property("cmake_target_name", "OpenTimelineIO::OpenTimelineIO")
        self.cpp_info.libs = ["opentime","opentimelineio"]
