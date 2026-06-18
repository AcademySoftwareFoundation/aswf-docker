# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

import os
from conan import ConanFile
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv
from conan.tools.files import copy, get, rm, rmdir
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps
from conan.tools.layout import basic_layout

required_conan_version = ">=1.54.0"


class LibmicrohttpdConan(ConanFile):
    name = "libmicrohttpd"
    description = "A small C library that is supposed to make it easy to run an HTTP server"
    homepage = "https://www.gnu.org/software/libmicrohttpd/"
    topics = ("httpd", "server", "service")
    license = "LGPL-2.1"
    url = "https://github.com/conan-io/conan-center-index"
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_https": [True, False],
        "with_zlib": [True, False],
        "with_error_messages": [True, False],
        "with_postprocessor": [True, False],
        "with_digest_authentification": [True, False],
        "epoll": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_https": True,
        "with_zlib": True,
        "with_error_messages": True,
        "with_postprocessor": True,
        "with_digest_authentification": True,
        "epoll": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            del self.options.epoll
        if self.settings.os != "Linux":
            del self.options.epoll

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")

    def layout(self):
        basic_layout(self, src_folder="src")

    def requirements(self):
        if self.options.with_zlib:
            self.requires("zlib/[>=1.2.11 <2]")
        if self.options.get_safe("with_https"):
            self.requires("gnutls/[>=3 <4]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        VirtualBuildEnv(self).generate()
        VirtualRunEnv(self).generate(scope="build")
        yes_no = lambda v: "yes" if v else "no"
        tc = AutotoolsToolchain(self)
        tc.configure_args.extend([
            f"--enable-shared={yes_no(self.options.shared)}",
            f"--enable-static={yes_no(not self.options.shared)}",
            f"--enable-https={yes_no(self.options.with_https)}",
            f"--enable-zlib={yes_no(self.options.with_zlib)}",
            f"--enable-messages={yes_no(self.options.with_error_messages)}",
            f"--enable-postprocessor={yes_no(self.options.with_postprocessor)}",
            f"--enable-dauth={yes_no(self.options.with_digest_authentification)}",
            f"--enable-epoll={yes_no(self.options.get_safe('epoll', default=False))}",
            "--disable-doc",
            "--disable-examples",
            "--disable-curl",
        ])
        tc.generate()
        AutotoolsDeps(self).generate()

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        # ASWF: separate licenses per package to avoid /usr/local/ collisions
        copy(self, "COPYING", src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses", self.name))
        autotools = Autotools(self)
        autotools.install()
        rm(self, "*.la", os.path.join(self.package_folder, "lib"))
        # ASWF: keep cmake files, delete pkgconfig files
        #rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("pkg_config_name", "libmicrohttpd")
        self.cpp_info.libs = ["microhttpd"]
        if self.settings.os in ["FreeBSD", "Linux"]:
            self.cpp_info.system_libs = ["pthread"]
