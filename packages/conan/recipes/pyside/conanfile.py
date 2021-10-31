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
    settings = (
        "os",
        "arch",
        "compiler",
        "build_type",
        "ci_common",
        "vfx_platform",
        "python",
    )
    generators = "cmake_find_package_multi"

    _source_subfolder = "source_subfolder"

    def requirements(self):
        self.requires(
            f"python/{os.environ['ASWF_PYTHON_VERSION']}@{self.user}/{self.channel}"
        )
        self.requires(f"qt/{os.environ['ASWF_QT_VERSION']}@{self.user}/{self.channel}")

    def build_requirements(self):
        self.build_requires(
            f"clang/{os.environ['ASWF_CLANG_VERSION']}@{self.user}/ci_common{self.settings.ci_common}"
        )

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename(
            self.conan_data["sources"][self.version]["url"]
            .split("/")[-1]
            .replace(".tar.xz", ""),
            self._source_subfolder,
        )
        if self.version == "5.12.6":
            # Apply typing patch
            tools.get(
                "https://codereview.qt-project.org/changes/pyside%2Fpyside-setup~271412/revisions/4/patch?zip",
                filename="typing-patch.zip",
            )
            self.run("patch -p1 < ../28958df.diff", cwd=self._source_subfolder)
            # Apply clang10 patch
            tools.get(
                "https://codereview.qt-project.org/changes/pyside%2Fpyside-setup~296271/revisions/2/patch?zip",
                filename="clang10-patch.zip",
            )
            self.run("patch -p1 < ../9ae6382.diff", cwd=self._source_subfolder)

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
