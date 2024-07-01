# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile
from conan.errors import ConanException
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conans import tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "arch", "build_type", "python"
    generators = "CMakeToolchain", "CMakeDeps", "VirtualRunEnv"

    def _boost_option(self, name, default):
        try:
            return getattr(self.options["boost"], name, default)
        except (AttributeError, ConanException):
            return default

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["WITH_PYTHON"] = not self.options["boost"].without_python
        if not self.options["boost"].without_python:
            pyversion = tools.Version(self.settings.python)
            tc.cache_variables["Python_ADDITIONAL_VERSIONS"] = "{}.{}".format(
                pyversion.major, pyversion.minor
            )
            tc.cache_variables["PYTHON_COMPONENT_SUFFIX"] = "{}{}".format(
                pyversion.major, pyversion.minor
            )
        tc.cache_variables["WITH_RANDOM"] = not self.options["boost"].without_random
        tc.cache_variables["WITH_REGEX"] = not self.options["boost"].without_regex
        tc.cache_variables["WITH_TEST"] = not self.options["boost"].without_test
        tc.cache_variables["WITH_COROUTINE"] = not self.options[
            "boost"
        ].without_coroutine
        tc.cache_variables["WITH_CHRONO"] = not self.options["boost"].without_chrono
        tc.cache_variables["WITH_LOCALE"] = not self.options["boost"].without_locale
        tc.cache_variables["WITH_NOWIDE"] = not self._boost_option(
            "without_nowide", True
        )
        tc.cache_variables["WITH_JSON"] = not self._boost_option("without_json", True)
        if not self.options["boost"].without_stacktrace:
            tc.cache_variables["WITH_STACKTRACE"] = True
            tc.cache_variables["WITH_STACKTRACE_ADDR2LINE"] = True
        tc.generate()

    def build(self):
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def test(self):
        if tools.cross_building(self.settings):
            return
        self.run(os.path.join("bin", "lambda_exe"), run_environment=True)
        if not self.options["boost"].without_random:
            self.run(os.path.join("bin", "random_exe"), run_environment=True)
        if not self.options["boost"].without_regex:
            self.run(os.path.join("bin", "regex_exe"), run_environment=True)
        if not self.options["boost"].without_test:
            self.run(os.path.join("bin", "test_exe"), run_environment=True)
        if not self.options["boost"].without_coroutine:
            self.run(os.path.join("bin", "coroutine_exe"), run_environment=True)
        if not self.options["boost"].without_chrono:
            self.run(os.path.join("bin", "chrono_exe"), run_environment=True)
        if not self.options["boost"].without_locale:
            self.run(os.path.join("bin", "locale_exe"), run_environment=True)
        if not self._boost_option("without_nowide", True):
            self.run(
                "{} {}".format(
                    os.path.join("bin", "nowide_exe"),
                    os.path.join(self.source_folder, "conanfile.py"),
                ),
                run_environment=True,
            )
        if not self._boost_option("without_json", True):
            self.run(os.path.join("bin", "json_exe"), run_environment=True)
        if not self.options["boost"].without_python:
            with tools.environment_append({"PYTHONPATH": "{}:{}".format("bin", "lib")}):
                pyversion = tools.Version(self.settings.python)
                self.run(
                    f"python{pyversion.major}.{pyversion.minor} {os.path.join(self.source_folder, 'python.py')}",
                    run_environment=True,
                )
            self.run(os.path.join("bin", "numpy_exe"), run_environment=True)
        if not self.options["boost"].without_stacktrace:
            self.run(os.path.join("bin", "stacktrace_noop_exe"), run_environment=True)
            self.run(
                os.path.join("bin", "stacktrace_addr2line_exe"), run_environment=True
            )
            if self.settings.os == "Windows":
                self.run(
                    os.path.join("bin", "stacktrace_windbg_exe"), run_environment=True
                )
                self.run(
                    os.path.join("bin", "stacktrace_windbg_cached_exe"),
                    run_environment=True,
                )
            else:
                self.run(
                    os.path.join("bin", "stacktrace_basic_exe"), run_environment=True
                )
            if self._boost_option("with_stacktrace_backtrace", False):
                self.run(
                    os.path.join("bin", "stacktrace_backtrace_exe"),
                    run_environment=True,
                )
