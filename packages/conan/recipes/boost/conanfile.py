# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conans import AutoToolsBuildEnvironment, ConanFile, tools
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.layout import basic_layout
from contextlib import contextmanager
from conan.tools.files import (
    apply_conandata_patches,
    collect_libs,
    copy,
    export_conandata_patches,
    get,
    rmdir,
)
import os

CONFIGURE_OPTIONS = (
    "atomic",
    "chrono",
    "container",
    "context",
    "coroutine",
    "date_time",
    "exception",
    "fiber",
    "filesystem",
    "graph",
    "graph_parallel",
    "iostreams",
    "locale",
    "log",
    "math",
    "mpi",
    "program_options",
    "python",
    "random",
    "regex",
    "serialization",
    "stacktrace",
    "system",
    "test",
    "thread",
    "timer",
    "type_erasure",
    "wave",
)


class BoostConan(ConanFile):
    name = "boost"
    settings = (
        "os",
        "arch",
        "compiler",
        "build_type",
        "python",
    )
    description = "Boost provides free peer-reviewed portable C++ source libraries"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    homepage = "https://www.boost.org"
    license = "BSL-1.0"
    topics = "conan", "boost", "libraries", "cpp", ""
    generators = "pkg_config"

    options = {}
    options.update(
        {"without_{}".format(_name): [True, False] for _name in CONFIGURE_OPTIONS}
    )

    default_options = {}
    default_options.update(
        {"without_{}".format(_name): False for _name in CONFIGURE_OPTIONS}
    )

    generators = "cmake"

    def _with_component(self, comp):
        return not self.options.get_safe(f"without_{comp}", False)

    def requirements(self):
        if self._with_component("python"):
            self.requires(
                f"python/{os.environ['ASWF_PYTHON_VERSION']}@{self.user}/{self.channel}"
            )

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        basic_layout(self, src_folder="src")
        # We want DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        build_args = [
            "./b2",
            "install",
            "-j2",
            "variant=release",
            "toolset=gcc",
            "link=shared",
            "-j%s" % tools.cpu_count(),
            "--abbreviate-paths",
            f"--prefix={self.package_folder}",
            f"--build-dir={self.build_folder}",
            f"--libdir={os.path.join(self.package_folder,'lib64')}",
        ]
        for comp in CONFIGURE_OPTIONS:
            if self._with_component(comp):
                build_args.append(f"--with-{comp}")
            else:
                build_args.append(f"--without-{comp}")

        if self._with_component("python"):
            python_version = tools.Version(self.dependencies["python"].ref.version)
            major_minor = f"{python_version.major}.{python_version.minor}"
            py_jam = os.path.join(self.source_folder, "python-config.jam")
            with open(py_jam, "w") as f:
                jam = [
                    "using python",
                    major_minor,
                    f"{self.deps_cpp_info['python'].bin_paths[0]}/{self.deps_user_info['python'].python_interp}",
                    self.deps_cpp_info["python"].include_paths[0],
                    self.deps_cpp_info["python"].lib_paths[0],
                ]
                f.write(" : ".join(jam) + " ;\n")
                print("!!! JAM=" + " : ".join(jam) + " ;\n")

            self.run(
                f"sh bootstrap.sh --with-python=bin/python{major_minor} --with-python-version={major_minor}",
                cwd=self.source_folder,
                run_environment=True,
            )
            build_args.append(f"--user-config={py_jam}")
        else:
            self.run("sh bootstrap.sh", cwd=self.source_folder, run_environment=True)
        if not self.version.startswith("1.61"):
            build_args.append("cxxstd=14")

        self.run(" ".join(build_args), cwd=self.source_folder, run_environment=True)

    def package(self):
        copy(
            self,
            "LICENSE_1_0.txt",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses", self.name),
        )

    def package_info(self):
        self.env_info.BOOST_ROOT = self.package_folder

        self.env_info.CMAKE_PREFIX_PATH.append(
            os.path.join(self.package_folder, "lib64", "cmake")
        )

        self.cpp_info.filenames["cmake_find_package"] = "Boost"
        self.cpp_info.filenames["cmake_find_package_multi"] = "Boost"
        self.cpp_info.names["cmake_find_package"] = "Boost"
        self.cpp_info.names["cmake_find_package_multi"] = "Boost"

        # - Use 'headers' component for all includes + defines
        # - Use '_libboost' component to attach extra system_libs, ...

        self.cpp_info.components["headers"].libs = []
        self.cpp_info.components["headers"].names["cmake_find_package"] = "headers"
        self.cpp_info.components["headers"].names[
            "cmake_find_package_multi"
        ] = "headers"
        self.cpp_info.components["headers"].names["pkg_config"] = "boost"

        # Boost::boost is an alias of Boost::headers
        self.cpp_info.components["_boost_cmake"].requires = ["headers"]
        self.cpp_info.components["_boost_cmake"].names["cmake_find_package"] = "boost"
        self.cpp_info.components["_boost_cmake"].names[
            "cmake_find_package_multi"
        ] = "boost"

        self.cpp_info.components["_libboost"].requires = ["headers"]
        if self.settings.os == "Linux":
            # https://github.com/conan-community/community/issues/135
            self.cpp_info.components["_libboost"].system_libs.append("rt")
            self.cpp_info.components["_libboost"].system_libs.append("pthread")

        for comp in CONFIGURE_OPTIONS:
            if not self._with_component(comp):
                continue
            self.cpp_info.components[comp].requires = ["headers"]

        if self._with_component("atomic"):
            self.cpp_info.components["atomic"].libs = ["boost_atomic"]
        if self._with_component("chrono"):
            self.cpp_info.components["chrono"].libs = ["boost_chrono"]
            self.cpp_info.components["chrono"].requires.append("system")
        if self._with_component("container"):
            self.cpp_info.components["container"].libs = ["boost_container"]
        if self._with_component("context"):
            self.cpp_info.components["context"].libs = ["boost_context"]
        if self._with_component("coroutine"):
            self.cpp_info.components["coroutine"].libs = ["boost_coroutine"]
            self.cpp_info.components["coroutine"].requires.append("system")
        if self._with_component("date_time"):
            self.cpp_info.components["date_time"].libs = ["boost_date_time"]
        if self._with_component("filesystem"):
            self.cpp_info.components["filesystem"].libs = ["boost_filesystem"]
        if self._with_component("graph"):
            self.cpp_info.components["graph"].libs = ["boost_graph"]
        if self._with_component("iostreams"):
            self.cpp_info.components["iostreams"].libs = ["boost_iostreams"]
        if self._with_component("locale"):
            self.cpp_info.components["locale"].libs = ["boost_locale"]
        if self._with_component("log_setup"):
            self.cpp_info.components["log_setup"].libs = ["boost_log_setup"]
        if self._with_component("log"):
            self.cpp_info.components["log"].libs = ["boost_log"]
        if self._with_component("math"):
            self.cpp_info.components["math"].libs = [
                "boost_math_c99f",
                "boost_math_c99l",
                "boost_math_c99",
                "boost_math_tr1f",
                "boost_math_tr1l",
                "boost_math_tr1",
            ]
        if self._with_component("program_options"):
            self.cpp_info.components["program_options"].libs = ["boost_program_options"]
        if self._with_component("python"):
            python_version = tools.Version(self.dependencies["python"].ref.version)
            major_minor = f"{python_version.major}{python_version.minor}"
            if python_version >= "3":
                suffix = major_minor
            else:
                suffix = ""
            self.cpp_info.components["python"].libs = [f"boost_python{suffix}"]
            self.cpp_info.components["python"].requires.append("python::PythonLibs")
            self.cpp_info.components[f"python{major_minor}"].requires.append("python")
            self.cpp_info.components["numpy"].libs = [f"boost_numpy{suffix}"]
            self.cpp_info.components["numpy"].requires.append("python")
            self.cpp_info.components[f"numpy{major_minor}"].requires.append("numpy")
        if self._with_component("random"):
            self.cpp_info.components["random"].libs = ["boost_random"]
        if self._with_component("regex"):
            self.cpp_info.components["regex"].libs = ["boost_regex"]
        if self._with_component("serialization"):
            self.cpp_info.components["serialization"].libs = [
                "boost_serialization",
                "boost_wserialization",
            ]
        if self._with_component("stacktrace"):
            self.cpp_info.components["stacktrace_addr2line"].requires = [
                "headers",
                "stacktrace",
            ]
            self.cpp_info.components["stacktrace_addr2line"].libs = [
                "boost_stacktrace_addr2line"
            ]
            self.cpp_info.components["stacktrace_basic"].requires = [
                "headers",
                "stacktrace",
            ]
            self.cpp_info.components["stacktrace_basic"].libs = [
                "boost_stacktrace_basic"
            ]
            self.cpp_info.components["stacktrace_noop"].requires = [
                "headers",
                "stacktrace",
            ]
            self.cpp_info.components["stacktrace_noop"].libs = ["boost_stacktrace_noop"]
            if self.settings.os in ("Linux", "FreeBSD"):
                self.cpp_info.components["stacktrace_basic"].system_libs.append("dl")
                self.cpp_info.components["stacktrace_noop"].system_libs.append("dl")
                self.cpp_info.components["stacktrace_addr2line"].system_libs.append(
                    "dl"
                )
        if self._with_component("system"):
            self.cpp_info.components["system"].libs = ["boost_system"]
            self.cpp_info.components["system"].requires.append("_libboost")
        if self._with_component("thread"):
            self.cpp_info.components["thread"].libs = ["boost_thread"]
        if self._with_component("timer"):
            self.cpp_info.components["timer"].libs = ["boost_timer"]
        if self._with_component("type_erasure"):
            self.cpp_info.components["type_erasure"].libs = ["boost_type_erasure"]
        if self._with_component("unit_test_framework"):
            self.cpp_info.components["unit_test_framework"].libs = [
                "boost_prg_exec_monitor",
                "boost_unit_test_framework",
            ]
        if self._with_component("wave"):
            self.cpp_info.components["wave"].libs = ["boost_wave"]

    def deploy(self):
        self.copy("*", symlinks=True)
