from conans import ConanFile, tools, CMake
import os

required_conan_version = ">=1.38.0"


class OpenEXRConan(ConanFile):
    name = "openexr"
    description = "The OpenEXR project provides the specification and reference implementation of the EXR file format, the professional-grade image storage format of the motion picture industry."
    topics = "conan", "openexr", "python", "binding"
    homepage = "https://www.qt.io/qt-for-python"
    license = "LGPL-3.0"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    settings = (
        "os",
        "arch",
        "compiler",
        "build_type",
        "python",
    )

    _cmake = None
    _source_subfolder = "source_subfolder"

    def requirements(self):
        self.requires(f"python/(latest)@{self.user}/{self.channel}")
        self.requires(f"boost/(latest)@{self.user}/{self.channel}")
        if tools.Version(self.version) >= "3":
            self.requires(f"imath/(latest)@{self.user}/{self.channel}")

    def build_requirements(self):
        self.build_requires(f"cmake/(latest)@{self.user}/{self.channel}")

    def source(self):
        tools.get(
            f"https://github.com/AcademySoftwareFoundation/openexr/archive/v{self.version}.tar.gz"
        )
        os.rename(f"openexr-{self.version}", self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        with tools.environment_append(tools.RunEnvironment(self).vars):
            self._cmake = CMake(self)
            self._cmake.definitions["OPENEXR_BUILD_PYTHON_LIBS"] = "ON"
            self._cmake.definitions["PYTHON_INCLUDE_DIR"] = self.deps_cpp_info[
                "python"
            ].include_paths[0]
            self._cmake.definitions["PYTHON_LIBRARY"] = self.deps_cpp_info[
                "python"
            ].lib_paths[0]
            self._cmake.definitions["BOOST_INCLUDEDIR"] = self.deps_cpp_info[
                "boost"
            ].include_paths[0]
            self._cmake.definitions["BOOST_LIBRARYDIR"] = self.deps_cpp_info[
                "boost"
            ].lib_paths[0]
            self._cmake.configure(source_folder=self._source_subfolder)
            return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.md", src=self._source_subfolder, dst="licenses")
        if (
            tools.Version(self.version).major == "2"
            and tools.Version(self.version).minor == "3"
        ):
            self.copy(
                "FindOpenEXR.cmake",
                src=os.path.join(self._source_subfolder, "cmake"),
                dst=os.path.join("lib", "cmake"),
            )
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.requires.append("python::PythonLibs")
        self.cpp_info.requires.append("boost::python")
        pymajorminor = self.deps_user_info["python"].python_interp
        self.env_info.PYTHONPATH.append(
            os.path.join(self.package_folder, "lib", pymajorminor, "site-packages")
        )
        if (
            tools.Version(self.version).major == "2"
            and tools.Version(self.version).minor == "3"
        ):
            self.env_info.CMAKE_MODULE_PATH.append(
                os.path.join(self.package_folder, "lib", "cmake")
            )
        else:
            self.env_info.CMAKE_PREFIX_PATH.append(
                os.path.join(self.package_folder, "lib", "cmake")
            )

        self.cpp_info.filenames["cmake_find_package"] = "OpenEXR"
        self.cpp_info.filenames["cmake_find_package_multi"] = "OpenEXR"
        self.cpp_info.libs = ["IlmImf", "IlmImfUtils"]
        if tools.Version(self.version) >= "3":
            self.cpp_info.requires.append("imath::imath")
