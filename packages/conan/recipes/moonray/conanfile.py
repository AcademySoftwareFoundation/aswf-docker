# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile

required_conan_version = ">=2.1"


class MoonrayConan(ConanFile):
    name = "moonray"
    description = (
        "MoonRay renderer — Conan meta-package declaring all build "
        "dependencies needed to compile MoonRay. This package installs no "
        "binaries itself; it exists so that 'conan install --requires=moonray/X' "
        "will pull in the complete set of MoonRay build prerequisites."
    )
    license = "Apache-2.0"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"
    homepage = "https://github.com/OpenMoonRay/openmoonray"
    topics = ("rendering", "vfx", "aswf", "moonray")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def requirements(self):
        # ---- VFX Reference Platform packages ----
        # Versions below are defaults for VFX Platform 2024; the aswf/vfx202X
        # Conan profiles will override these via [replace_requires] pins.
        self.requires("boost/1.82.0")
        self.requires("cpython/3.11.13")
        self.requires("imath/3.1.12")
        self.requires("opencolorio/2.3.2")
        self.requires("openexr/3.2.9")
        self.requires("openimageio/2.5.19.1")
        self.requires("opensubdiv/3.6.1")
        self.requires("openusd/24.08")
        self.requires("openvdb/11.0.0")
        self.requires("onetbb/2020.3")

        # ---- Additional upstream dependencies ----
        self.requires("freetype/2.13.2")
        self.requires("glfw/3.4")          # hydra/hdMoonray GL viewport
        self.requires("libjpeg-turbo/3.0.4")
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires("openssl/system")
        self.requires("opengl/system")

        # ---- MoonRay-specific dependencies ----
        self.requires("embree/4.2.0")         # SIMD ray traversal
        self.requires("jsoncpp/1.9.5")        # scene_rdl2 JSON I/O
        self.requires("libcgroup/0.42.2")     # arras compute-node control groups
        self.requires("libmicrohttpd/0.9.72") # arras HTTP server
        self.requires("log4cplus/2.1.2")      # logging (scene_rdl2)
        self.requires("lua/5.4.4")            # shader DSO scripting
        self.requires("openimagedenoise/2.3.3")  # mcrt_denoise
        self.requires("random123/1.14.0")     # stochastic sampling

    def package_id(self):
        self.info.clear()
