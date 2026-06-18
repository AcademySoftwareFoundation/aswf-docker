# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

import os
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get, rmdir
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps
from conan.tools.layout import basic_layout

required_conan_version = ">=2.1"


class LibcgroupConan(ConanFile):
    name = "libcgroup"
    description = (
        "libcgroup is a library that abstracts Linux cgroup filesystem operations. "
        "Used by OpenMoonRay's Arras distribution layer."
    )
    license = "LGPL-2.1-only"
    url = "https://github.com/libcgroup/libcgroup"
    homepage = "https://github.com/libcgroup/libcgroup"
    topics = ("cgroups", "linux", "containers", "resources")
    package_type = "shared-library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }

    def validate(self):
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration(f"{self.ref} is only available on Linux")

    def layout(self):
        basic_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
            destination=self.source_folder, strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        if self.options.fPIC:
            tc.extra_cflags.append("-fPIC")
        tc.configure_args += [
            "--disable-tests",
            "--disable-samples",
            "--disable-pam",
        ]
        tc.generate()
        deps = AutotoolsDeps(self)
        deps.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        copy(self, "COPYING",
             src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses", self.name))
        autotools = Autotools(self)
        autotools.install()
        # Remove .la files and pkgconfig (ASWF convention)
        for pattern in ("*.la",):
            for f in self._find_files(os.path.join(self.package_folder, "lib"), pattern):
                os.remove(f)
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def _find_files(self, root, pattern):
        import fnmatch
        matches = []
        for dirpath, _, files in os.walk(root):
            for fname in files:
                if fnmatch.fnmatch(fname, pattern):
                    matches.append(os.path.join(dirpath, fname))
        return matches

    def package_info(self):
        self.cpp_info.libs = ["cgroup"]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread"]
