# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 The Foundry Visionmongers Ltd

import os
import sys
import glob
import shutil
import platform

from conan import ConanFile
from conan.tools.env import Environment
from conan.tools.scm import Version
from conan.errors import ConanException
from conan.tools.files import copy, get, export_conandata_patches, apply_conandata_patches


class PySide6Conan(ConanFile):
    name = "pyside"
    license = "LGPL-3.0"
    author = "The Qt Company"
    url = "git://code.qt.io/pyside/pyside-setup.git"
    description = "PySide6 is the official Python module from the 'Qt for Python project', which provides access to the complete Qt 6+ framework"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True],
        "python_version": [os.environ["ASWF_PYTHON_MAJOR_MINOR_VERSION"]],
    }
    # revision_mode = 'scm'
    package_originator = "External"
    package_exportable = True

    default_options = {
        "shared": True,
        "python_version": os.environ["ASWF_PYTHON_MAJOR_MINOR_VERSION"],
    }
    no_copy_source = True
    short_paths = True

    executables = [
        "shiboken",
        "lupdate",
    ]

    @property
    def _useOpenGLBackend(self):
        return self.options.GLBackend == "OpenGL"

    def requirements(self):
        self.requires(f"cpython/{os.environ['ASWF_CPYTHON_VERSION']}@{self.user}/{self.channel}")
        self.requires(f"qt/{os.environ['ASWF_QT_VERSION']}@{self.user}/{self.channel}")
        self.requires(f"clang/{os.environ['ASWF_PYSIDE_CLANG_VERSION']}@{self.user}/ci_common{os.environ['CI_COMMON_VERSION']}")
        self.requires(f"md4c/{os.environ['ASWF_MD4C_VERSION']}@{self.user}/{self.channel}")

    def build_requirements(self):
        self.tool_requires(
            f"ninja/{os.environ['ASWF_NINJA_VERSION']}@{self.user}/ci_common{os.environ['CI_COMMON_VERSION']}"
        )

        # Assume already installed
        # if self.settings.os == "Linux":
        #    self.build_requires("patchelf")

        # Windows needs separate shiboken package built in release mode due to a stack overflow
        # when running shiboken built in Debug from source (also related to libclang)
        if self.settings.os == "Windows":
            self.tool_requires(f"pyside-shiboken/{self.version}")

    def export_sources(self):
        export_conandata_patches(self)

    def configure(self):
        # self.options["qt"].with_webengine = False
        # self.options["qt"].with_vulkan = True
        pass

    @property
    def _checkout_folder(self):
        return "{}_src".format(self.name)

    def source(self):
        destination = os.path.join(self.source_folder, self._checkout_folder)
        if platform.system() == "Windows":
            # Don't use os.path.join, or it removes the \\?\ prefix, which enables long paths
            destination = rf"\\?\{self.source_folder}"
        get(
            self,
            **self.conan_data["sources"][self.version],
            strip_root=True,
            destination=destination,
        )

        # patching in source method because of no_copy_source attribute
        apply_conandata_patches(self)

    @property
    def pythonLocalRoot(self):
        # Windows uses a local copy of the Python libs, see import() for details
        return os.path.join(self.install_folder, "python")

    def imports(self):
        if self.settings.os == "Windows":
            # Windows uses a local copy of the Python library.
            # This copy has the "Python*.zip" file removed. If this is not removed, a number of systems
            # try to load and/or modify file from this ZIP file, and fail.
            # To avoid this, we copy the Python conan package into the install directory and use it.
            self.copy(
                pattern="*",
                root_package="python",
                dst=self.pythonLocalRoot,
                excludes="Python*.zip",
            )

    def _set_r_paths(self, binaries, rpath=""):
        if self.settings.os == "Linux":
            if rpath != "":
                rpath = "/" + rpath
            # Assume installed on system
            # patchelfPath = os.path.join(self.dependencies["patchelf"].cpp_info.bin_paths[0], "patchelf")
            patchelfPath = "/usr/bin/patchelf"
            for bin in binaries:
                self.run(f"{patchelfPath} --set-rpath \$ORIGIN{rpath} {bin}")
        if self.settings.os == "Macos":
            for bin in binaries:
                self.run(f"install_name_tool -add_rpath {rpath} {bin}")

    def _buildCommand(self, pythonBinPath, srcDir, qmakePath):
        # TODO Skip some modules, RemoteObjects was added by KDAB.
        # Will anyone care if these are missing?
        skipModules = ["RemoteObjects"]

        self.run(f"{pythonBinPath} -m ensurepip")

        # see https://bugreports.qt.io/browse/PYSIDE-1385 for the version choice of wheel
        # index_url = "https://an_artifactory_url/artifactory/api/pypi/PyPI_Virtual/simple"
        index_url = "https://pypi.org/simple"
        self.run(
            f"{pythonBinPath} -m pip install -qq wheel==0.34.2 packaging --index-url {index_url}"
        )

        args = [
            pythonBinPath,
            os.path.join(srcDir, "setup.py"),
            "build",
            "--qtpaths",
            qmakePath,
            "--verbose-build",
            "--skip-modules",
            ",".join(skipModules),
            "--make-spec",
            "ninja",
            "--parallel",
            str(os.cpu_count()),
            "--ignore-git",
            "--reuse-build",
        ]
        if self.settings.build_type == "Debug":
            args.append("--debug")
        return " ".join(args)

    def _buildLinux(self, srcDir):
        qtInfo = self.dependencies["qt"]
        qtBinPath = qtInfo.cpp_info.bindirs[0]
        qmakePath = os.path.join(qtBinPath, "qtpaths6")

        llvmInfo = self.dependencies["clang"]

        pythonInfo = self.dependencies["cpython"]
        pythonBinPath = os.path.join(
            pythonInfo.package_folder,
            pythonInfo.cpp_info.bindirs[0],
            "python"
        )

        # Shiboken finds the C++ includes from gcc-toolset but fails to add C includes,
        # so cstddef doesn't find stddef.h for instance.
        # This is not elegant but not clear how to do it differetly.

        env = Environment()
        env.define("LLVM_INSTALL_DIR", llvmInfo.package_folder)
        env.define("LD_LIBRARY_PATH", pythonInfo.cpp_info.libdirs[0])
        # Something in Qt depends on md4c
        md4cInfo = self.dependencies["md4c"]
        env.append("LD_LIBRARY_PATH", md4cInfo.cpp_info.libdirs[0],separator=':')
        env.define("CMAKE_PREFIX_PATH", f"{qtInfo.package_folder}:{llvmInfo.package_folder}")
        env.define("CPATH", f"/opt/rh/gcc-toolset-{os.environ['ASWF_DTS_VERSION']}/root/usr/lib/gcc/x86_64-redhat-linux/{os.environ['ASWF_DTS_VERSION']}/include")
        env_vars = env.vars(self)

        with env_vars.apply():
            buildCmd = self._buildCommand(pythonBinPath, srcDir, qmakePath)
            self.run(buildCmd)

            installBinDir = os.path.join(self._installDir, "bin")

            # self._set_r_paths([os.path.join(installBinDir, exe) for exe in self.executables])

            # Copy the shared libraries shiboken needs to be able to run into the package
            for lib in ("Core", "Gui", "Network", "OpenGL", "Widgets", "Xml"):
                for f in glob.glob(
                    os.path.join(qtInfo.package_folder, "lib64", f"libQt6{lib}.so*")
                ):
                    shutil.copy(f, installBinDir, follow_symlinks=False)
            for f in glob.glob(
                os.path.join(llvmInfo.package_folder, "lib64", "libclang.so*")
            ):
                shutil.copy(f, installBinDir, follow_symlinks=False)

    def _buildMac(self, srcDir):
        qtInfo = self.dependencies["qt"]
        qtBinPath = qtInfo.cpp_info.bin_paths[0]
        qmakePath = os.path.join(qtBinPath, "qtpaths6")

        llvmInfo = self.dependencies["clang"]

        pythonInfo = self.dependencies["cpython"]
        pythonBinPath = os.path.join(
            pythonInfo.cpp_info.bin_paths[0], self.dependencies["cpython"].conf_info.python_interp
        )

        env = Environment()
        env.define("LLVM_INSTALL_DIR", llvmInfo.package_folder)
        env.define("CMAKE_PREFIX_PATH", f"{qtInfo.package_folder}:{llvmInfo.package_folder}")
        env.defiine("CXXFLAGS", f"-I{pythonInfo.cpp_info.includedirs[0]}")
        env_vars = env.vars(self)

        with env_vars.apply():
            buildCmd = self._buildCommand(pythonBinPath, srcDir, qmakePath)
            self.run(buildCmd)

    def _buildWindows(self, srcDir):
        qtInfo = self.dependencies["qt"]
        qtBinPath = qtInfo.cpp_info.bin_paths[0]
        qmakePath = os.path.join(qtBinPath, "qtpaths6.exe")

        llvmInfo = self.dependencies["clang"]

        pythonBinPath = os.path.join(
            self.pythonLocalRoot, "bin", self.dependencies["cpython"].conf_info.python_interp
        )

        # from Python 3.8 DLL loading is more restrictive, disallowing PATH, see https://bugs.python.org/issue43173
        # use os.add_dll_directory to ensure Qt6.dll is available.
        os.add_dll_directory(qtBinPath)
        os.environ["PATH"] += os.pathsep + qtBinPath

        env = Environment()
        env.define("LLVM_INSTALL_DIR", llvmInfo.package_folder)
        env.define("CMAKE_PREFIX_PATH", f"{qtInfo.package_folder}:{llvmInfo.package_folder}")
        env.define("CC", "cl.exe")  # pic up MSVC rather than clang from LLVM
        env.define("CXX", "cl.exe")
        env_vars = env.vars(self)

        with env_vars.apply():
            # don't run the full build in one go, as that fails in Debug builds due to a stack overflow
            # in (Debug) libclang while running shiboken - bring in a release build of shiboken to build PySide6
            # seems to be related to https://bugreports.qt.io/browse/PYSIDE-739

            buildCmd = self._buildCommand(pythonBinPath, srcDir, qmakePath)
            self.run(buildCmd + " --build-type=shiboken")

            shibokenInfo = self.dependencies["pyside-shiboken"]
            installBinDir = os.path.join(self._installDir, "bin")
            for f in glob.glob(os.path.join(shibokenInfo.package_folder, "bin", "*")):
                shutil.copy(f, installBinDir)

            self.run(buildCmd + " --build-type=pyside")

    def build(self):
        srcDir = os.path.join(self.source_folder, self._checkout_folder)
        if self.settings.os == "Linux":
            self._buildLinux(srcDir)
        elif self.settings.os == "Macos":
            self._buildMac(srcDir)
        elif self.settings.os == "Windows":
            self._buildWindows(srcDir)
        else:
            raise RuntimeError("Recipe not implemented for this OS")

    @property
    def _installDir(self):
        pythonVersion = Version(self.dependencies["cpython"].ref.version)
        pythonVersionMajorMinor = f"{pythonVersion.major}.{pythonVersion.minor}"
        qtVersion = self.dependencies["qt"].ref.version

        src_dir = os.path.join(self.source_folder, self._checkout_folder)

        # pyside is using the venv name to contain the install dir.
        # see https://a_gitlab_url/libraries/conan/thirdparty/pyside/pyside/-/commit/0a40ebb1
        # venv_name = os.path.basename(sys.prefix)
        # Not sure what's the best way to do this, but this is unlikely to be it
        venv_name = f"qfp-py{pythonVersionMajorMinor}-qt{qtVersion}-64bit-"
        if self.settings.build_type == "Debug":
            venv_name += "debug"
        else:
            venv_name += "release"

        install_dir = os.path.join(src_dir, "build", venv_name, "install")
        if not os.path.isdir(install_dir):
            raise ConanException(f"Could not find the install directory {install_dir}")

        return install_dir

    def _configure_package_mac(self):
        # self._set_r_paths(
        #    [os.path.join(self.package_folder, 'bin', exe) for exe in self.executables],
        #    '@executable_path'
        # )

        # Copy the DLLs shiboken needs to be able to run into the package
        for lib in ("Core", "Gui", "Network", "OpenGL", "Qml", "Widgets", "Xml"):
            framework = f"Qt{lib}.framework"
            self.copy(
                src=os.path.join(self.dependencies["qt"].cpp_info.lib_paths[0], framework),
                pattern="*",
                dst=f"bin/{framework}",
            )
            self.copy(
                src=os.path.join(self.dependencies["qt"].cpp_info.lib_paths[0], framework),
                pattern="*",
                dst=f"lib64/{framework}",
            )

        self.copy(
            src=os.path.join(self.dependencies["clang"].package_folder, "lib64"),
            pattern="libclang.dylib",
            dst="bin",
        )

        def _getFilesByExt(searchDir, ext):
            files = []
            for file in os.listdir(searchDir):
                fullFilePath = os.path.join(searchDir, file)
                if not os.path.islink(fullFilePath) and file.endswith(ext):
                    files.append(fullFilePath)
            return files

        libDir = os.path.join(self.package_folder, "lib64")
        libs = _getFilesByExt(libDir, ".dylib")
        # self._set_r_paths(libs, '@loader_path/../bin')

        v = Version(self.dependencies["cpython"].ref.version)
        sitePkgDir = os.path.join(
            self.package_folder, f"lib64/python{v.major}.{v.minor}/site-packages"
        )

        libDir = os.path.join(self.package_folder, sitePkgDir, "shiboken")
        libs = _getFilesByExt(libDir, ".so")
        # self._set_r_paths(libs, '@loader_path/../../../')

        libDir = os.path.join(self.package_folder, sitePkgDir, "PySide")
        libs = _getFilesByExt(libDir, ".so")
        # self._set_r_paths(libs, '@loader_path/../../../')
        # self._set_r_paths(libs, '@loader_path/../../../../bin')

    def package(self):
        copy(self,pattern="*", src=self._installDir, dst=self.package_folder )
        # copy(self,pattern="*", src="cmake", dst="cmake")

        if self.settings.os == "Macos":
            self._configure_package_mac()

        # Shiboken needs LLVM available on Linux to be able to determine
        # system include paths while parsing. For simplicity, just copying
        # the whole package into this one.
        #
        # Let's not do that as it hugely increases the size of the package,
        # let Conan install the right dependencies
        #
        # if self.settings.os == "Linux":
        #     copy(self,pattern="*", src=self.deps_cpp_info["clang"].package_folder, dst="clang")

    def package_info(self):
        v = Version(self.dependencies["cpython"].ref.version)
        if self.settings.os == "Windows":
            self.user_info.site_package = os.path.join(
                self.package_folder, "lib64/site-packages"
            )
        else:
            self.user_info.site_package = os.path.join(
                self.package_folder, f"lib64/python{v.major}.{v.minor}/site-packages"
            )
