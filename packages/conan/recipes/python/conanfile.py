from conans import AutoToolsBuildEnvironment, ConanFile, tools
from contextlib import contextmanager
from conan.tools.files.symlinks import absolute_to_relative_symlinks
from conan.tools.files import (
    apply_conandata_patches,
    collect_libs,
    copy,
    export_conandata_patches,
    get,
    rmdir,
)
from jinja2 import Environment, FileSystemLoader

from semver import SemVer
import os
import sysconfig
import re


class PythonConan(ConanFile):
    name = "python"
    description = "Python is a programming language that lets you work quickly and integrate systems more effectively."
    topics = ("conan", "python")
    license = "Python (PSF-2.0 license) and numpy (BSD-3-Clause license)"
    homepage = "https://python.org/"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    settings = (
        "os",
        "arch",
        "compiler",
        "build_type",
        "python",
    )
    options = {"with_numpy": [True, False]}
    default_options = {"with_numpy": True}
    generators = "pkg_config"
    exports_sources = "*.cmake"

    _autotools = None

    def configure(self):
        python_version = tools.Version(self.version)
        self.major_minor = f"{python_version.major}.{python_version.minor}"
        if "ASWF_NUMPY_VERSION" not in os.environ:
            self.options.with_numpy.value = False

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def export_sources(self):
        export_conandata_patches(self)
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
            "--with-platlibdir=lib64",
            "--libdir=${prefix}/lib64",
        ]
        self._autotools.configure(args=conf_args)
        return self._autotools

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        with self._build_context():
            self._patch_sources()
            autotools = self._configure_autotools()
            autotools.make()

    @property
    def _abi_suffix(self):
        v = SemVer(self.version, False)
        if self.settings.os == "Windows":
            return f"{v.major}{v.minor}{self._exe_suffix}"
        else:
            return "{}.{}{}{}".format(
                v.major,
                v.minor,
                "d" if self.settings.build_type == "Debug" and v.major >= 3 else "",
                "m" if (v.major >= 3 and v.minor < 8) or v.major > 3 else "",
            )

    def _produce_config_files(self):
        p = os.path.join(self.package_folder, "lib64", "cmake", "python")
        if not os.path.exists(p):
            os.makedirs(p, exist_ok=True)

        pyver = SemVer(self.version, False)
        file_loader = FileSystemLoader(self.source_folder)
        env = Environment(loader=file_loader)

        def _configure(file_name):
            data = {
                "version_major": str(pyver.major),
                "version_minor": str(pyver.minor),
                "version_patch": str(pyver.patch),
                "os": self.settings.os,
                "bt": self.settings.build_type,
                "abi_suffix": self._abi_suffix,
            }

            interpreter_template = env.get_template(file_name)
            interpreter_template.stream(data).dump(
                os.path.join(self.package_folder, "lib64", "cmake", "python", file_name)
            )

        _configure("Python_InterpreterTargets.cmake")
        _configure("Python_DevelopmentTargets.cmake")
        _configure("Python_Macros.cmake")
        _configure("PythonConfig.cmake")
        _configure("PythonConfigVersion.cmake")

    def package(self):
        self._produce_config_files()

        copy(
            self,
            "COPYING",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses", self.name),
        )

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
        py_exe_nover = os.path.join(self.package_folder, "bin", f"python")
        self.run(f"ln -s {py_exe} {py_exe_nover}")

        with tools.environment_append(
            {
                "PATH": os.path.join(self.package_folder, "bin"),
                "LD_LIBRARY_PATH": os.path.join(self.package_folder, "lib64"),
            }
        ):
            self.run(f"{py_exe} get-pip.py")

            # Replace first line of pip to fix the hardcoded shebang line
            def _replaceShebang(script_prefix):
                script_folder = os.path.join(self.package_folder, "bin")
                for name in os.listdir(script_folder):
                    if not name.startswith(script_prefix):
                        continue
                    script = os.path.join(script_folder, name)
                    with open(script) as f:
                        lines = f.readlines()
                    lines[0] = "#!/usr/bin/env python3\n"
                    with open(script, "w") as f:
                        f.writelines(lines)

            _replaceShebang("pip")
            _replaceShebang("wheel")
            _replaceShebang("2to3-")

            # FIXME: how do you convince pip to write to lib64 instead of lib?
            self.run(f"{py_exe} -m pip install nose coverage docutils epydoc")
            if self.options.get_safe("with_numpy"):
                self.run(
                    f"{py_exe} -m pip install numpy=={os.environ['ASWF_NUMPY_VERSION']}"
                )

        absolute_to_relative_symlinks(self, self.package_folder)

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
        self.cpp_info.components["PythonLibs"].libdirs = [
            "lib64",
            "lib",
        ]
        if self.settings.os == "Windows":
            self.cpp_info.components["PythonLibs"].defines.append("PYTHON_DLL")

    def deploy(self):
        self.copy("*", symlinks=True)

        # Something of a hack: the generated _sysconfigdata__PLATFORM.py embeds build paths
        # This breaks tools that use sysconfig to find Python's INCLUDEDIR such as Qt.
        # deploy() is only called by conan install package_reference

        tools.replace_in_file(
            os.path.join(
                self.install_folder,
                f"lib64/python{self.major_minor}/_sysconfigdata__{sysconfig.get_config_var('MACHDEP')}_{sysconfig.get_config_var('MULTIARCH')}.py",
            ),
            re.sub(
                r"^/opt/conan_home", r"/tmp/c", self.package_folder
            ),  # FIXME is there a better way? aswfdocker defines CONAN_USER_HOME
            self.install_folder,
            strict=False,  # don't complain if it was already done in persistent cache
        )
