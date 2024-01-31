from conans import ConanFile, tools, CMake
import os

required_conan_version = ">=1.38.0"


class ImathConan(ConanFile):
    name = "imath"
    description = "Imath is a C++ and python library of 2D and 3D vector, matrix, and math operations for computer graphics."
    topics = "conan", "imath", "python", "vfx"
    homepage = "https://github.com/AcademySoftwareFoundation/Imath"
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

    def _is_dummy(self):
        return tools.Version(self.version) < "3"

    def requirements(self):
        if self._is_dummy():
            return
        self.requires(
            f"python/{os.environ['ASWF_PYTHON_VERSION']}@{self.user}/{self.channel}"
        )
        self.requires(
            f"boost/{os.environ['ASWF_BOOST_VERSION']}@{self.user}/{self.channel}"
        )

    def build_requirements(self):
        if self._is_dummy():
            return
        self.build_requires(
            f"cmake/{os.environ['ASWF_CMAKE_VERSION']}@{self.user}/{self.channel}"
        )

    def source(self):
        if self._is_dummy():
            with open("imath-2-is-a-dummy-package.txt", "w") as f:
                f.write(
                    "Imath only contains data starting from version 3. Use OpenEXR-2 for Imath-2"
                )
        else:
            tools.get(
                f"https://github.com/AcademySoftwareFoundation/Imath/archive/v{self.version}.tar.gz"
            )
            os.rename(f"Imath-{self.version}", self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        with tools.environment_append(tools.RunEnvironment(self).vars):
            self._cmake = CMake(self)
            self._cmake.definitions["PYTHON"] = "ON"
            self._cmake.configure(source_folder=self._source_subfolder)
            return self._cmake

    def build(self):
        if not self._is_dummy():
            cmake = self._configure_cmake()
            cmake.build()

    def package(self):
        if self._is_dummy():
            self.copy("imath-2-is-a-dummy-package.txt")
        else:
            self.copy("LICENSE.md", src=self._source_subfolder, dst="licenses")
            cmake = self._configure_cmake()
            cmake.install()

    def package_info(self):
        if self._is_dummy():
            self.user_info.is_dummy = True
            return
        self.user_info.is_dummy = False
        self.cpp_info.requires.append("python::PythonLibs")
        self.cpp_info.requires.append("boost::python")
        pymajorminor = self.deps_user_info["python"].python_interp
        self.env_info.PYTHONPATH.append(
            os.path.join(self.package_folder, "lib", pymajorminor, "site-packages")
        )
        self.env_info.CMAKE_PREFIX_PATH.append(
            os.path.join(self.package_folder, "lib", "cmake")
        )

    def deploy(self):
        self.copy("*")
