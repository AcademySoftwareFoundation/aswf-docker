# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 The Foundry Visionmongers Ltd

from os import path, environ, pathsep
from conans import ConanFile, CMake
from conans.model.version import Version
from contextlib import contextmanager


@contextmanager
def _patch_env_vars(env_var_dict):
    original = dict(environ)
    environ.update(env_var_dict)
    yield
    environ.clear()
    environ.update(original)


class TestPackage(ConanFile):
    settings = "os", "arch", "compiler", "build_type"

    generators = ["cmake_paths"]

    def configure(self):
        del self.settings.compiler.libcxx

    @property
    def pythonVersion(self):
        return Version("3.9.10")

    @property
    def libPaths(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            return [
                *self.deps_cpp_info["pyside"].lib_paths,
                *self.deps_cpp_info["qt"].lib_paths,
            ]
        if self.settings.os == "Windows":
            return [
                *self.deps_cpp_info["pyside"].bin_paths,
                *self.deps_cpp_info["qt"].bin_paths,
            ]

    @property
    def sitePkgPath(self):
        basePath = self.deps_cpp_info["pyside"].lib_paths[0]
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            return path.join(
                basePath,
                f"python{self.pythonVersion.as_list[0]}.{self.pythonVersion.as_list[1]}",
                "site-packages",
            )

        if self.settings.os == "Windows":
            return path.join(basePath, "site-packages")

    @property
    def testEnvVars(self):
        env = {
            "PYTHONPATH": self.sitePkgPath,
            "QT_PLUGIN_PATH": path.join(self.deps_cpp_info["qt"].rootpath, "plugins"),
        }

        if self.settings.os == "Windows":
            env["FN_PYTHON_DLL_DIRECTORIES"] = pathsep.join(self.libPaths)
        elif self.settings.os == "Linux":
            env["LD_LIBRARY_PATH"] = pathsep.join(self.libPaths)

        return env

    def test(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_PROJECT_PackageTest_INCLUDE"] = path.join(
            self.install_folder, "conan_paths.cmake"
        )
        cmake.definitions["CONAN_PYTHON_VERSION"] = str(self.pythonVersion)
        cmake.definitions["CONAN_PYSIDE_VERSION"] = str(
            self.deps_cpp_info["pyside"].version
        )
        cmake.definitions["Python_ROOT_DIR"] = self.deps_cpp_info["python"].rootpath
        if self.settings.os == "Macos":
            cmake.definitions["CMAKE_FIND_FRAMEWORK"] = "LAST"

        with _patch_env_vars(self.testEnvVars):
            cmake.configure()
            cmake.build()
            cmake.test(output_on_failure=True)
