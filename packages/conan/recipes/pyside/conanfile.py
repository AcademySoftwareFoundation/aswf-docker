from conans import ConanFile, tools
import os

required_conan_version = ">=1.38.0"


class PySideConan(ConanFile):
    name = "pyside"
    description = "Seamless operability between C++11 and Python"
    topics = "conan", "pyside", "python", "binding"
    homepage = "https://www.qt.io/qt-for-python"
    license = "LGPL-3.0"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    exports = ["patches/*.diff"]
    settings = (
        "os",
        "arch",
        "compiler",
        "build_type",
        "python",
    )
    generators = "cmake_find_package_multi"

    _source_subfolder = "source_subfolder"

    def requirements(self):
        self.requires(f"python/(latest)@{self.user}/{self.channel}")
        self.requires(f"qt/(latest)@{self.user}/{self.channel}")

    def build_requirements(self):
        self.build_requires(
            f"clang/(latest)@{self.user}/ci_common{os.environ['CI_COMMON_VERSION']}"
        )

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extractdir = (
            self.conan_data["sources"][self.version]["url"]
            .split("/")[-1]
            .replace(".tar.xz", "")
        )
        if self.version == "5.15.9":
            # tar file for 5.15.9 adds -1 suffix, but extracts to 5.15.9
            extractdir = extractdir.rstrip("-1")
        os.rename(
            extractdir,
            self._source_subfolder,
        )
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)

    def build(self):
        vars = tools.RunEnvironment(self).vars
        vars.update(
            {
                "Qt5_DIR": self.build_folder,
            }
        )
        with tools.environment_append(vars):
            self.run(
                f"{self.deps_cpp_info['python'].bin_paths[0]}/{self.deps_user_info['python'].python_interp} setup.py build --parallel={tools.cpu_count()}",
                cwd=self._source_subfolder,
            )

    def package(self):
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses")
        # Unfortunately the "instal" command still does a lot of building...
        self.run(
            f"{self.deps_cpp_info['python'].bin_paths[0]}/{self.deps_user_info['python'].python_interp} setup.py install --prefix {self.package_folder}",
            cwd=self._source_subfolder,
            run_environment=True,
        )

    def package_info(self):
        self.cpp_info.requires.append("python::PythonLibs")
        self.cpp_info.requires.append("qt::qt")
        pymajorminor = self.deps_user_info["python"].python_interp
        self.env_info.PYTHONPATH.append(
            os.path.join(self.package_folder, "lib", pymajorminor, "site-packages")
        )

    def deploy(self):
        self.copy("*")
