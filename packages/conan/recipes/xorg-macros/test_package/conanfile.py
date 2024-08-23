# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

import os

from conan import ConanFile
from conan.tools.gnu import AutotoolsToolchain, Autotools
from conan.tools.layout import basic_layout


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    test_type = "explicit"
    win_bash = True

    @property
    def _settings_build(self):
        return self.settings_build if hasattr(self, "settings_build") else self.settings

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)
        self.build_requires(
            f"automake/{os.environ['ASWF_AUTOMAKE_VERSION']}@{self.user}/{self.channel}"
        )
        if self._settings_build.os == "Windows" and not self.conf.get(
            "tools.microsoft.bash:path", check_type=str
        ):
            self.tool_requires("msys2/cci.latest")

    def layout(self):
        basic_layout(self, src_folder="src")

    def generate(self):
        tc = AutotoolsToolchain(self)
        tc.generate()

    def build(self):
        # Only make sure the project configures correctly, as these are build scripts
        autotools = Autotools(self)
        autotools.autoreconf(args=["--debug"])
        autotools.configure()

    def test(self):
        # FIXME: how to test extra pkg_config content?
        pass
