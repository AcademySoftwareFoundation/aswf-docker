# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/7abb9ee39e6009e3dbc45043307a1098246d4ad7/recipes/b2/portable/conanfile.py

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import cross_building
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import chdir, copy, get
from conan.tools.layout import basic_layout

from contextlib import contextmanager
import os
from io import StringIO

required_conan_version = ">=1.47.0"


class B2Conan(ConanFile):
    name = "b2"
    homepage = "https://www.bfgroup.xyz/b2/"
    description = "B2 makes it easy to build C++ projects, everywhere."
    topics = ("installer", "builder", "build", "build-system")
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch"
    package_type = "application"

    '''
    * use_cxx_env: False, True

    Indicates if the build will use the CXX and
    CXXFLAGS environment variables. The common use is to add additional flags
    for building on specific platforms or for additional optimization options.

    * toolset: 'auto', 'cxx', 'cross-cxx',
    'acc', 'borland', 'clang', 'como', 'gcc-nocygwin', 'gcc',
    'intel-darwin', 'intel-linux', 'intel-win32', 'kcc', 'kylix',
    'mingw', 'mipspro', 'pathscale', 'pgi', 'qcc', 'sun', 'sunpro',
    'tru64cxx', 'vacpp', 'vc12', 'vc14', 'vc141', 'vc142', 'vc143'

    Specifies the toolset to use for building. The default of 'auto' detects
    a usable compiler for building and should be preferred. The 'cxx' toolset
    uses the 'CXX' and 'CXXFLAGS' solely for building. Using the 'cxx'
    toolset will also turn on the 'use_cxx_env' option. And the 'cross-cxx'
    toolset uses the 'BUILD_CXX' and 'BUILD_CXXFLAGS' vars. This frees the
    'CXX' and 'CXXFLAGS' variables for use in subprocesses.
    '''
    options = {
        'use_cxx_env': [False, True],
        'toolset': [
            'auto', 'cxx', 'cross-cxx',
            'acc', 'borland', 'clang', 'como', 'gcc-nocygwin', 'gcc',
            'intel-darwin', 'intel-linux', 'intel-win32', 'kcc', 'kylix',
            'mingw', 'mipspro', 'pathscale', 'pgi', 'qcc', 'sun', 'sunpro',
            'tru64cxx', 'vacpp', 'vc12', 'vc14', 'vc141', 'vc142', 'vc143',
        ]
    }
    default_options = {
        'use_cxx_env': False,
        'toolset': 'auto'
    }

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        del self.info.options.use_cxx_env
        del self.info.options.toolset

        if self._is_macos_intel_or_arm(self.info.settings):
            self.info.settings.arch = "x86_64,armv8"

    def validate_build(self):
        if hasattr(self, "settings_build") and cross_building(self) and not self._is_macos_intel_or_arm(self.settings):
            raise ConanInvalidConfiguration(f"{self.ref} recipe doesn't support cross-build yet")

    def validate(self):
        if (self.options.toolset == 'cxx' or self.options.toolset == 'cross-cxx') and not self.options.use_cxx_env:
            raise ConanInvalidConfiguration(
                "Option toolset 'cxx' and 'cross-cxx' requires 'use_cxx_env=True'")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    @property
    def _b2_dir(self):
        return self.source_folder

    @property
    def _b2_engine_dir(self):
        return os.path.join(self._b2_dir, "src", "engine")

    @property
    def _b2_output_dir(self):
        return os.path.join(self.build_folder, "output")

    @property
    def _pkg_bin_dir(self):
        return os.path.join(self.package_folder, "bin")

    def _is_macos_intel_or_arm(self, settings):
        return settings.os == "Macos" and settings.arch in ["x86_64", "armv8"]

    @contextmanager
    def _bootstrap_env(self):
        saved_env = dict(os.environ)
        # Vcvars will change the directory after it runs in the situation when
        # the user has previously run the VS command console inits. In that
        # context it remembers the dir and resets it at each vcvars invocation.
        os.environ.update({"VSCMD_START_DIR": os.getcwd()})
        if not self.options.use_cxx_env:
            # To avoid using the CXX env vars we clear them out for the build.
            os.environ.update({
                "CXX": "",
                "CXXFLAGS": ""})
        try:
            yield
        finally:
            os.environ.clear()
            os.environ.update(saved_env)

    def _write_project_config(self, cxx):
        with open(os.path.join(self.source_folder, "project-config.jam"), "w") as f:
            f.write(
                f"using {self.options.toolset} : : {cxx} ;\n"
            )

    def build(self):
        # The order of the with:with: below is important. The first one changes
        # the current dir. While the second does env changes that guarantees
        # that dir doesn't change if/when vsvars runs to set the msvc compile
        # env.
        self.output.info("Build engine..")
        command = ""
        b2_toolset = self.options.toolset
        use_windows_commands = os.name == 'nt'
        if b2_toolset == 'auto':
            if use_windows_commands:
                # For windows auto detection it can evaluate to a msvc version
                # that it's not aware of. Most likely because it's a future one
                # that didn't exist when the build was written. This turns that
                # into a generic msvc toolset build assuming it could work,
                # since it's a better version.
                with chdir(self, self._b2_engine_dir):
                    with self._bootstrap_env():
                        buf = StringIO()
                        self.run('guess_toolset && set', buf)
                        guess_vars = map(
                            lambda x: x.strip(), buf.getvalue().split("\n"))
                        if "B2_TOOLSET=vcunk" in guess_vars:
                            b2_toolset = 'msvc'
                            for kv in guess_vars:
                                if kv.startswith("B2_TOOLSET_ROOT="):
                                    b2_vcvars = os.path.join(
                                        kv.split('=')[1].strip(), 'Auxiliary', 'Build', 'vcvars32.bat')
                                    command += '"'+b2_vcvars+'" && '
        command += "build" if use_windows_commands else "./build.sh"

        cxxflags = ""
        if self._is_macos_intel_or_arm(self.settings):
            cxxflags += " -arch arm64 -arch x86_64"

        if self.options.use_cxx_env:
            envvars = VirtualBuildEnv(self).vars()

            cxx_env = envvars.get("CXX")
            if cxx_env:
                command += f" --cxx={cxx_env}"
                self._write_project_config(cxx_env)

            cxxflags_env = envvars.get("CXXFLAGS")
            if cxxflags_env:
                cxxflags = f"{cxxflags} {cxxflags_env}"

        if cxxflags:
            command += f' --cxxflags="{cxxflags}"'

        if b2_toolset != 'auto':
            command += " "+str(b2_toolset)
        with chdir(self, self._b2_engine_dir):
            with self._bootstrap_env():
                self.run(command)

        self.output.info("Install..")
        command = os.path.join(
            self._b2_engine_dir, "b2.exe" if use_windows_commands else "b2")
        if b2_toolset not in ["auto", "cxx", "cross-cxx"]:
            command += " toolset=" + str(b2_toolset)
        full_command = \
            (f"{command} --ignore-site-config " +
             f"--prefix={self._b2_output_dir} " +
             "--abbreviate-paths " +
             "install " +
             "b2-install-layout=portable")
        with chdir(self, self._b2_dir):
            self.run(full_command)

    def package(self):
        copy(self, "LICENSE.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        copy(self, "*.LICENSE", src=self._b2_engine_dir, dst=os.path.join(self.package_folder, "licenses", self.name))
        copy(self, "*b2", dst=self._pkg_bin_dir, src=self._b2_output_dir)
        copy(self, "*b2.exe", dst=self._pkg_bin_dir, src=self._b2_output_dir)
        copy(self, "*.jam", dst=self._pkg_bin_dir, src=self._b2_output_dir)

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []

        # TODO: to remove in conan v2
        self.env_info.PATH.append(self._pkg_bin_dir)
