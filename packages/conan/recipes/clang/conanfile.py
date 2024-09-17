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
from conan.tools.microsoft import is_msvc
from conans import tools
import os


class ClangConan(ConanFile):
    name = "clang"
    description = (
        "A toolkit for the construction of highly optimized compilers,"
        "optimizers, and runtime environments."
    )
    license = "Apache-2.0 WITH LLVM-exception"
    topics = ("conan", "llvm", "clang")
    homepage = "https://github.com/llvm/llvm-project/tree/master/llvm"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "components": "ANY",
        "targets": "ANY",
    }
    default_options = {
        "components": "clang;clang-tools-extra;lld",
        "targets": "host;NVPTX",
    }

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")
        # We want DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def build_requirements(self):
        self.build_requires(
            f"ninja/{os.environ['ASWF_NINJA_VERSION']}@{self.user}/ci_common{os.environ['CI_COMMON_VERSION']}"
        )
        # if tools.Version(self.version) > "11":
        # We can't use our python package for a few reasons:
        # - it introduces a circular dependency between the clang package build, in ci_commonX context
        #   and vfx20XX context
        # - the Package ID won't match: the vfx20XX profile adds a python=3.x setting which the ci_commonX
        #   doesn't have, and if you don't define ASWF_NUMPY_VERSION, the conanfile.py for the python package
        #   sets the option with_numpy=False, which also invalidates the Package ID
        #
        # Also the process which installed Conan in our build container built a Python in /tmp/pyconan, but
        # it cleans up up once Conan has been installed and turned into an executable with pyinstaller.
        #
        # As of VFX 2023 we can assume a reasonably recent Python 3 in the base image.
        #
        # self.build_requires(f"python/3.9.7@{self.user}/vfx2022")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["GCC_INSTALL_PREFIX"] = tools.get_env("GCC_INSTALL_PREFIX")
        tc.variables["LLVM_BUILD_LLVM_DYLIB"] = True
        tc.variables["CLANG_INCLUDE_DOCS"] = False
        tc.variables["LIBCXX_INCLUDE_DOCS"] = False
        tc.variables["LLVM_BUILD_TESTS"] = False
        tc.variables["LLVM_INCLUDE_TESTS"] = False
        tc.variables["LLVM_INCLUDE_TOOLS"] = True
        tc.variables["LLVM_BUILD_TOOLS"] = True
        tc.variables["LLVM_TOOL_LLVM_AR_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_AS_BUILD"] = True
        tc.variables["LLVM_TOOL_LLVM_AS_FUZZER_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_BCANALYZER_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_COV_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_CXXDUMP_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_DIS_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_EXTRACT_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_C_TEST_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_DIFF_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_GO_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_JITLISTENER_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_LTO_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_MC_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_NM_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_OBJDUMP_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_PROFDATA_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_RTDYLD_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_SIZE_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_SPLIT_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_STRESS_BUILD"] = False
        tc.variables["LLVM_TOOL_LLVM_SYMBOLIZER_BUILD"] = True
        tc.variables["LLVM_INCLUDE_EXAMPLES"] = False
        tc.variables["CMAKE_SKIP_RPATH"] = True
        tc.variables["LLVM_ENABLE_PROJECTS"] = self.options.components
        tc.variables["LLVM_TARGETS_TO_BUILD"] = self.options.targets
        compiler = self.settings.compiler.value
        version = tools.Version(self.settings.compiler.version)
        if (
            tools.Version(self.version) >= "13"
            and compiler == "gcc"
            and int(version.major) >= 9
        ):
            # llvm-13 / gcc9 fails to build (mostly unused) libc++
            # see https://www.mail-archive.com/llvm-bugs@lists.llvm.org/msg53136.html
            tc.variables["LLVM_ENABLE_RUNTIMES"] = "compiler-rt"
            tc.variables["LLVM_TOOL_LIBCXX_BUILD"] = "OFF"
            tc.variables["LLVM_TOOL_LIBCXXABI_BUILD"] = "OFF"
        else:
            tc.variables["LLVM_ENABLE_RUNTIMES"] = "libcxx;libcxxabi;compiler-rt"
            tc.variables["LLVM_TOOL_LIBCXX_BUILD"] = "ON"
            tc.variables["LLVM_TOOL_LIBCXXABI_BUILD"] = "ON"
        tc.variables["LLVM_ENABLE_LIBXML2"] = "OFF"
        if self.settings.compiler == "Visual Studio":
            build_type = str(self.settings.build_type).upper()
            tc.variables[
                "LLVM_USE_CRT_{}".format(build_type)
            ] = self.settings.compiler.runtime
        # Libraries go to lib64
        tc.variables["LLVM_LIBDIR_SUFFIX"] = "64"
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure(build_script_folder="llvm")
        cmake.build()

    def package(self):
        copy(
            self,
            "LICENSE.TXT",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses", self.name),
        )
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib64", "pkgconfig"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        try:
            self.cpp_info.libs.remove("LLVMHello")
        except ValueError:
            pass
        try:
            self.cpp_info.libs.remove("BugpointPasses")
        except ValueError:
            pass
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread", "rt", "dl", "m", "curses"]
        elif self.settings.os == "Macos":
            self.cpp_info.system_libs = ["m"]
        self.env_info.LLVM_INSTALL_DIR = self.package_folder
        self.env_info.CLANG_INSTALL_DIR = self.package_folder

    def deploy(self):
        self.copy("*", symlinks=True)
