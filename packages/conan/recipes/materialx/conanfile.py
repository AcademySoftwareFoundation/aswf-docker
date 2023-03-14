from conans import ConanFile, tools, CMake
import os

required_conan_version = ">=1.38.0"


class MaterialXConan(ConanFile):
    name = "materialx"
    description = "MaterialX is an open standard for the exchange of rich material and look-development content across applications and renderers."
    topics = "conan", "materialx", "python", "vfx"
    homepage = "https://github.com/AcademySoftwareFoundation/MaterialX"
    license = "BSD-3-Clause"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    settings = (
        "os",
        "arch",
        "compiler",
        "build_type",
        "python",
    )
    generators = "cmake_find_package_multi"

    _cmake = None
    _source_subfolder = "source_subfolder"

    def requirements(self):
        self.requires(f"python/(latest)@{self.user}/{self.channel}")
        self.requires(f"pybind11/(latest)@{self.user}/{self.channel}")

    def build_requirements(self):
        self.build_requires(f"cmake/(latest)@{self.user}/{self.channel}")

    def source(self):
        tools.get(
            f"https://github.com/AcademySoftwareFoundation/MaterialX/archive/v{self.version}.tar.gz"
        )
        os.rename(f"MaterialX-{self.version}", self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        with tools.environment_append(tools.RunEnvironment(self).vars):
            self._cmake = CMake(self)
            self._cmake.definitions["MATERIALX_BUILD_PYTHON"] = "ON"
            self._cmake.configure(source_folder=self._source_subfolder)
            return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.md", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.requires.append("python::PythonLibs")
        self.cpp_info.requires.append("pybind11::main")
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "python"))
        self.env_info.CMAKE_PREFIX_PATH.append(
            os.path.join(self.package_folder, "lib", "cmake")
        )

    def deploy(self):
        self.copy("*")
