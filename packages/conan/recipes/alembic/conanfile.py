# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import (
    apply_conandata_patches,
    collect_libs,
    copy,
    export_conandata_patches,
    get,
    rmdir,
)
from conan.tools.scm import Version
import os

required_conan_version = ">=1.53.0"


class AlembicConan(ConanFile):
    name = "alembic"
    license = "BSD-3-Clause"
    description = "Alembic is an open framework for storing and sharing scene data that includes a C++ library, a file format, and client plugins and applications."
    topics = "conan", "alembic", "python", "binding"
    homepage = "https://www.alembic.io"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    package_type = "library"
    settings = (
        "os",
        "arch",
        "compiler",
        "build_type",
        "python",
    )
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_hdf5": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_hdf5": False,
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
        # We want DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def requirements(self):
        self.requires(
            f"python/{os.environ['ASWF_PYTHON_VERSION']}@{self.user}/{self.channel}"
        )
        self.requires(
            f"boost/{os.environ['ASWF_BOOST_VERSION']}@{self.user}/{self.channel}"
        )
        self.requires(
            f"imath/{os.environ['ASWF_IMATH_VERSION']}@{self.user}/{self.channel}"
        )
        self.requires(
            f"openexr/{os.environ['ASWF_OPENEXR_VERSION']}@{self.user}/{self.channel}"
        )

    def build_requirements(self):
        self.build_requires(
            f"cmake/{os.environ['ASWF_CMAKE_VERSION']}@{self.user}/{self.channel}"
        )

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["USE_ARNOLD"] = False
        tc.variables["USE_MAYA"] = False
        tc.variables["USE_PRMAN"] = False
        tc.variables["USE_PYALEMBIC"] = False
        tc.variables["USE_BINARIES"] = False
        tc.variables["USE_EXAMPLES"] = False
        tc.variables["USE_HDF5"] = self.options.with_hdf5
        tc.variables["USE_TESTS"] = False
        tc.variables["ALEMBIC_BUILD_LIBS"] = True
        tc.variables[
            "ALEMBIC_ILMBASE_LINK_STATIC"
        ] = False  # for -DOPENEXR_DLL, handled by OpenEXR package
        tc.variables["ALEMBIC_SHARED_LIBS"] = self.options.shared
        tc.variables["ALEMBIC_USING_IMATH_3"] = True
        tc.variables["ALEMBIC_ILMBASE_FOUND"] = 1
        tc.variables["ALEMBIC_ILMBASE_LIBS"] = "OpenEXR::OpenEXR"
        if Version(self.version) >= "1.8.4":
            tc.variables["ALEMBIC_DEBUG_WARNINGS_AS_ERRORS"] = False
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(
            self,
            "LICENSE.txt",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses", self.name),
        )
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))

    def package_info(self):
        self.cpp_info.requires.append("python::PythonLibs")
        self.cpp_info.requires.append("boost::python")
        pymajorminor = self.deps_user_info["python"].python_interp
        self.env_info.PYTHONPATH.append(
            os.path.join(self.package_folder, "lib64", pymajorminor, "site-packages")
        )

        # self.cpp_info.libs = ["IlmImf", "IlmImfUtils"]
        # if Version(self.version) >= "3":
        self.cpp_info.requires.append("Imath::Imath")

        self.cpp_info.set_property("cmake_file_name", "Alembic")
        self.cpp_info.set_property("cmake_target_name", "Alembic::Alembic")
        self.cpp_info.libs = ["Alembic"]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.extend(["m", "pthread"])

        # TODO: to remove in conan v2 once cmake_find_package* generators removed
        self.cpp_info.names["cmake_find_package"] = "Alembic"
        self.cpp_info.names["cmake_find_package_multi"] = "Alembic"

        self.env_info.CMAKE_PREFIX_PATH.append(
            os.path.join(self.package_folder, "lib64", "cmake")
        )

    def deploy(self):
        self.copy("*", symlinks=True)
