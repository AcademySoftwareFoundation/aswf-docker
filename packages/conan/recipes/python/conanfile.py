from platform import python_version
from conans import AutoToolsBuildEnvironment, ConanFile, tools
from contextlib import contextmanager
import os


class PythonConan(ConanFile):
    name = "python"
    description = "Python is the C++ port of the famous JUnit framework for unit testing. Test output is in XML for automatic testing and GUI based for supervised tests."
    topics = ("conan", "python", "unit-test", "tdd")
    license = " LGPL-2.1-or-later"
    homepage = "https://python.org/"
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
    options = {}
    default_options = {}
    generators = "pkg_config"

    _autotools = None

    def configure(self):
        python_version = tools.Version(self.version)
        self.major_minor = f"{python_version.major}.{python_version.minor}"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(
            f"https://www.python.org/ftp/python/{self.version}/Python-{self.version}.tgz"
        )
        os.rename(f"Python-{self.version}", self._source_subfolder)

    def export_sources(self):
        self.copy("run-with-system-python")
        self.copy("yum")

    @contextmanager
    def _build_context(self):
        if self.settings.compiler == "Visual Studio":
            with tools.vcvars(self.settings):
                env = {
                    "AR": "{} lib".format(
                        tools.unix_path(self.deps_user_info["automake"].ar_lib)
                    ),
                    "CC": "{} cl -nologo".format(
                        tools.unix_path(self.deps_user_info["automake"].compile)
                    ),
                    "CXX": "{} cl -nologo".format(
                        tools.unix_path(self.deps_user_info["automake"].compile)
                    ),
                    "NM": "dumpbin -symbols",
                    "OBJDUMP": ":",
                    "RANLIB": ":",
                    "STRIP": ":",
                }
                with tools.environment_append(env):
                    yield
        else:
            yield

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        self._autotools = AutoToolsBuildEnvironment(
            self, win_bash=tools.os_info.is_windows
        )
        if self.settings.os == "Windows":
            self._autotools.defines.append("PYTHON_BUILD_DLL")
        if self.settings.compiler == "Visual Studio":
            self._autotools.flags.append("-FS")
            self._autotools.cxx_flags.append("-EHsc")
        yes_no = lambda v: "yes" if v else "no"
        conf_args = [
            "--enable-shared=yes",
            "--enable-static=no",
            "--enable-debug={}".format(yes_no(self.settings.build_type == "Debug")),
            "--enable-doxygen=no",
            "--enable-dot=no",
            "--enable-werror=no",
            "--enable-html-docs=no",
        ]
        self._autotools.configure(args=conf_args, configure_dir=self._source_subfolder)
        return self._autotools

    def build(self):
        with self._build_context():
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        self.copy("COPYING", src=self._source_subfolder, dst="licenses")

        self.copy("yum", dst="bin")
        self.copy("run-with-system-python", dst="bin")

        with self._build_context():
            autotools = self._configure_autotools()
            autotools.install()

        python_version = tools.Version(self.version)
        if python_version.major == "3":
            tools.download(
                "https://bootstrap.pypa.io/get-pip.py", "get-pip.py", overwrite=True
            )
        else:
            tools.download(
                "https://bootstrap.pypa.io/pip/2.7/get-pip.py",
                "get-pip.py",
                overwrite=True,
            )

        py_exe = os.path.join(self.package_folder, "bin", f"python{self.major_minor}")
        with tools.environment_append(
            {
                "PATH": os.path.join(self.package_folder, "bin"),
                "LD_LIBRARY_PATH": os.path.join(self.package_folder, "lib"),
            }
        ):
            self.run(f"{py_exe} get-pip.py")
            self.run(
                f"{py_exe} -m pip install nose coverage docutils epydoc numpy=={os.environ['ASWF_NUMPY_VERSION']}"
            )

    def package_info(self):
        self.cpp_info.filenames["pkg_config"] = "python"
        self.user_info.python_interp = f"python{self.major_minor}"

        self.cpp_info.components["PythonInterp"].bindirs = ["bin"]

        self.cpp_info.components["PythonLibs"].requires = ["PythonInterp"]
        python_version = tools.Version(self.version)
        if python_version > "3.6" and python_version < 3.9:
            suffix = "m"
        else:
            suffix = ""
        self.cpp_info.components["PythonLibs"].includedirs = [
            f"include/python{self.major_minor}{suffix}"
        ]
        self.cpp_info.components["PythonLibs"].libs = [
            f"python{self.major_minor}{suffix}"
        ]
        if self.settings.os == "Windows":
            self.cpp_info.components["PythonLibs"].defines.append("PYTHON_DLL")
