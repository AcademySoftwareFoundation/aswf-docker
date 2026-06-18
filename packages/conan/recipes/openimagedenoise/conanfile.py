# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

import os
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get

required_conan_version = ">=2.1"


class OpenImageDenoiseConan(ConanFile):
    name = "openimagedenoise"
    description = (
        "Intel® Open Image Denoise is an open source library of high-performance, "
        "high-quality denoising filters for images rendered with ray tracing."
    )
    license = "Apache-2.0"
    url = "https://www.openimagedenoise.org/"
    homepage = "https://www.openimagedenoise.org/"
    topics = ("denoising", "rendering", "deep-learning", "intel")
    package_type = "shared-library"
    settings = "os", "arch"

    def validate(self):
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration(
                f"{self.ref} prebuilt binary is only available for Linux")
        if self.settings.arch != "x86_64":
            raise ConanInvalidConfiguration(
                f"{self.ref} prebuilt binary is only available for x86_64")

    def source(self):
        pass  # download in build() — self.settings not available in source()

    def build(self):
        arch = str(self.settings.arch)
        # tarball has a top-level dir: oidn-<ver>.x86_64.linux/
        get(self, **self.conan_data["sources"][self.version][arch],
            destination=self.build_folder, strip_root=True)

    def package(self):
        copy(self, "LICENSE.txt",
             src=os.path.join(self.build_folder, "doc"),
             dst=os.path.join(self.package_folder, "licenses", self.name))
        # Headers
        copy(self, "*",
             src=os.path.join(self.build_folder, "include"),
             dst=os.path.join(self.package_folder, "include"))
        # All OIDN shared libs; deliberately exclude the bundled TBB
        # (libtbb.so.12) that OIDN ships alongside itself — copying it
        # to /usr/local would overwrite the base-image TBB 2020.3 symlink
        # and break packages that rely on tbb::internal::* symbols.
        copy(self, "libOpenImageDenoise*",
             src=os.path.join(self.build_folder, "lib"),
             dst=os.path.join(self.package_folder, "lib"))
        # ASWF: keep cmake config files
        copy(self, "*",
             src=os.path.join(self.build_folder, "lib", "cmake"),
             dst=os.path.join(self.package_folder, "lib", "cmake"))
        # CLI tools (oidnDenoise, oidnTest, oidnBenchmark)
        copy(self, "*",
             src=os.path.join(self.build_folder, "bin"),
             dst=os.path.join(self.package_folder, "bin"))

    def package_id(self):
        # Binary-only: OS + arch only
        pass

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenImageDenoise")
        self.cpp_info.set_property("cmake_target_name", "OpenImageDenoise")
        self.cpp_info.libs = ["OpenImageDenoise"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.bindirs = ["bin"]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread", "dl", "m"]
