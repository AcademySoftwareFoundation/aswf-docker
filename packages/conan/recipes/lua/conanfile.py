# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

import os
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, load, save, collect_libs

required_conan_version = ">=2.1"


class LuaConan(ConanFile):
    name = "lua"
    description = "Lua is a powerful, efficient, lightweight, embeddable scripting language."
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.lua.org/"
    topics = ("embed", "scripting")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [False, True],
        "fPIC": [True, False],
        "compile_as_cpp": [True, False],
        "with_tools": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "compile_as_cpp": False,
        "with_tools": False,
    }

    def export_sources(self):
        copy(self, "CMakeLists.txt", src=self.recipe_folder,
             dst=self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        if not self.options.compile_as_cpp:
            self.options.rm_safe("compiler.libcxx")
            self.options.rm_safe("compiler.cppstd")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["LUA_SRC_DIR"] = self.source_folder.replace("\\", "/")
        tc.variables["COMPILE_AS_CPP"] = self.options.compile_as_cpp
        tc.variables["SKIP_INSTALL_TOOLS"] = not self.options.with_tools
        tc.variables["WITH_READLINE"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder,
                                                          os.pardir))
        cmake.build()

    def package(self):
        # Extract the license from the lua.h header (no standalone LICENSE file)
        # ASWF: separate licenses per package to avoid /usr/local/ collisions
        tmp = load(self, os.path.join(self.source_folder, "src", "lua.h"))
        license_contents = tmp[tmp.find("/***", 1):tmp.find("****/", 1) + 5]
        save(self, os.path.join(self.package_folder, "licenses", self.name,
                                "COPYING.txt"), license_contents)
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Lua")
        self.cpp_info.set_property("cmake_target_name", "Lua::Lua")
        self.cpp_info.set_property("pkg_config_name", "lua")
        self.cpp_info.libs = collect_libs(self)
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs = ["dl", "m"]
        if self.settings.os in ["Linux", "FreeBSD", "Macos"]:
            self.cpp_info.defines.extend(["LUA_USE_DLOPEN", "LUA_USE_POSIX"])
        elif self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.defines.append("LUA_BUILD_AS_DLL")
