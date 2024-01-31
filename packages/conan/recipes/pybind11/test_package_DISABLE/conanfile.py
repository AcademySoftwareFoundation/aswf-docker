from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import Environment, VirtualRunEnv
from conan.tools.build import can_run

import os
from pathlib import PurePath
import sys


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)
        self.requires(
            f"python/{os.environ['ASWF_PYTHON_VERSION']}@{self.user}/{self.channel}"
        )

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        toolchain = CMakeToolchain(self)
        # Used by FindPython.cmake in CMake
        toolchain.variables["Python_EXECUTABLE"] = PurePath(
            self._python_interpreter
        ).as_posix()
        # Used by FindPythonLibsNew.cmake in pybind11
        toolchain.variables["PYTHON_EXECUTABLE"] = PurePath(
            self._python_interpreter
        ).as_posix()
        toolchain.variables["Python_INCLUDE_DIR"] = self.deps_cpp_info[
            "python"
        ].include_paths[0]
        toolchain.variables["PYTHON_INCLUDE_DIRS"] = self.deps_cpp_info[
            "python"
        ].include_paths[0]
        toolchain.variables["Python_LIBRARY"] = self.deps_cpp_info["python"].lib_paths[
            0
        ]
        toolchain.variables["PYTHON_LIBRARIES"] = self.deps_cpp_info[
            "python"
        ].lib_paths[0]
        toolchain.generate()

        env = Environment()
        env.append_path(
            "PYTHONPATH", os.path.join(self.build_folder, self.cpp.build.libdirs[0])
        )
        env.vars(self, scope="run").save_script("testrun")

        run = VirtualRunEnv(self)
        run.generate()

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build(cli_args=["--verbose"])

    @property
    def _python_interpreter(self):
        return os.path.join(
            self.deps_cpp_info["python"].bin_paths[0],
            self.deps_user_info["python"].python_interp,
        )

    def test(self):
        if can_run(self):
            module_path = os.path.join(self.source_folder, "test.py")
            # FIXME: gross hack, how do we get DSO to have right name?
            self.run("mv test_package.cpython-39-x86_64-linux-gnu.so test_package.so")
            self.run(f'{self._python_interpreter} "{module_path}"', env="conanrun")
