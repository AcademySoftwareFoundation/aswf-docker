# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

import os
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv
from conan.tools.files import copy, get

required_conan_version = ">=2.1"


class IspcConan(ConanFile):
    name = "ispc"
    description = (
        "Intel® Implicit SPMD Program Compiler: a compiler for high-performance "
        "SIMD programming on CPUs and GPUs."
    )
    license = "BSD-3-Clause"
    url = "https://ispc.github.io/"
    homepage = "https://ispc.github.io/"
    topics = ("ispc", "compiler", "simd", "spmd")
    package_type = "application"
    settings = "os", "arch", "compiler", "build_type"

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration(
                f"{self.ref} build-from-source is currently Linux-only")
        if self.settings.arch not in ("x86_64", "armv8"):
            raise ConanInvalidConfiguration(
                f"{self.ref} is only available for x86_64 and armv8")

    def requirements(self):
        clang_ref = self.conf.get("user.aswf:ispc_clang_ref", check_type=str)
        # Host dep: LLVM headers and shared libraries linked into the ispc binary.
        self.requires(clang_ref, headers=True, libs=True)
        self.requires("onetbb/2023.0.0")

    def build_requirements(self):
        clang_ref = self.conf.get("user.aswf:ispc_clang_ref", check_type=str)
        # Tool dep: llvm-config, clang, clang++ … on PATH during cmake configure/build.
        self.tool_requires(clang_ref)
        self.tool_requires("cmake/[>=3.20 <4]")
        self.tool_requires("ninja/[>=1.0.0]")
        self.tool_requires("cpython/[>=3.9 <4]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def _ensure_gnu_stubs_32(self):
        if os.path.exists("/usr/include/gnu/stubs-32.h"):
            return
        # ISPC's 32-bit builtin generation compiles builtins-c-cpu.cpp with
        # -m32 --target=i686-unknown-linux-gnu even when only targeting x86_64.
        # glibc's stubs.h conditionally includes stubs-32.h which is only
        # provided by glibc-devel.i686. Rather than installing the full 32-bit
        # RPM (which drags in 32-bit runtime), download it and extract only the
        # two header files we need.
        self.run("dnf download --downloaddir=/tmp/ispc-rpms glibc-devel.i686")
        self.run(
            "rpm2cpio /tmp/ispc-rpms/glibc-devel-*.i686.rpm | "
            "cpio -id ./usr/include/gnu/stubs-32.h ./usr/include/gnu/lib-names-32.h",
            cwd="/"
        )

    def generate(self):
        # _ensure_gnu_stubs_32() is Linux/x86_64-specific (glibc-devel.i686 has
        # no armv8 equivalent). validate() currently allows armv8 too, so this
        # will need revisiting for ARM support.
        if self.settings.os == "Linux" and self.settings.arch == "x86_64":
            self._ensure_gnu_stubs_32()
        # Build env: puts llvm-config, clang, etc. from tool_requires on PATH.
        VirtualBuildEnv(self).generate()
        # Run env (scope="build"): LLVM DSOs on LD_LIBRARY_PATH so cmake sub-
        # processes that invoke clang/llvm-config can find the shared libraries.
        VirtualRunEnv(self).generate(scope="build")

        tc = CMakeToolchain(self, generator="Ninja")
        # Always link against LLVM DSOs — the clang recipe builds shared LLVM only.
        tc.variables["ISPC_STATIC_LINK"] = False
        tc.variables["ISPC_NO_DUMPS"] = True
        tc.variables["ISPC_INCLUDE_EXAMPLES"] = False
        tc.variables["ISPC_INCLUDE_TESTS"] = False
        tc.variables["ISPC_INCLUDE_BENCHMARKS"] = False
        # Enable only the LLVM backend that matches the build architecture;
        # the clang package is built with the host target only (no cross-targets).
        tc.variables["X86_ENABLED"] = self.settings.arch == "x86_64"
        tc.variables["ARM_ENABLED"] = self.settings.arch == "armv8"
        # Bake the Conan-cache LLVM lib dir into RPATH so the ispc binary
        # finds LLVM DSOs both in the cache and after patchelf relocation.
        tc.variables["CMAKE_INSTALL_RPATH_USE_LINK_PATH"] = True
        tc.variables["CMAKE_BUILD_WITH_INSTALL_RPATH"] = True
        tc.generate()
        CMakeDeps(self).generate()

    def build(self):
        cmake = CMake(self)
        # VirtualRunEnv ensures LLVM DSOs are on LD_LIBRARY_PATH for cmake
        # configure child processes (llvm-config, clang invocations in cmake).
        with VirtualRunEnv(self).vars().apply():
            cmake.configure()
            cmake.build()

    def package(self):
        copy(self, "LICENSE.txt",
             src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses", self.name))
        cmake = CMake(self)
        cmake.install()

    def package_id(self):
        # ispc is a standalone application; the C++ compiler used to build it
        # does not affect the package's identity from a consumer's perspective.
        del self.info.settings.compiler

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.set_property("cmake_find_mode", "none")
        ispc_bin = os.path.join(self.package_folder, "bin", "ispc")
        # Downstream CMake consumers can locate the ispc compiler via conf.
        self.conf_info.define("user.ispc:compiler", ispc_bin)
        # Expose ispc on PATH for consumers' build environments.
        self.buildenv_info.define_path("ISPC", ispc_bin)
        self.runenv_info.prepend_path("PATH", os.path.join(self.package_folder, "bin"))
