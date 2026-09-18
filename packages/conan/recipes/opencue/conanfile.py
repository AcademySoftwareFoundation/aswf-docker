# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile

required_conan_version = ">=2.1"


class OpenCueConan(ConanFile):
    name = "opencue"
    description = (
        "OpenCue — Conan meta-package declaring all build "
        "dependencies needed to compile OpenCue. This package installs no "
        "binaries itself; it exists so that 'conan install --requires=opencue/X' "
        "will pull in the complete set of OpenCue build prerequisites."
    )
    license = "Apache-2.0"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    homepage = "https://github.com/AcademySoftwareFoundation/OpenCue"
    topics = ("rendering", "vfx", "aswf", "opencue")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def requirements(self):
        # ---- Core Python & Runtime Environment ----
        self.requires("cpython/3.11.13")
        
        # ---- GUI & PySide (for CueGUI / Cuetopia) ----
        self.requires("pyside/6.5.3")

        # ---- Networking, Security & Serialization ----
        self.requires("openssl/3.3.1")
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires("jsoncpp/1.9.5")

        # ---- Foundational Utilities ----
        self.requires("boost/1.82.0")
        self.requires("imath/3.1.12")

    def package_id(self):
        self.info.clear()
