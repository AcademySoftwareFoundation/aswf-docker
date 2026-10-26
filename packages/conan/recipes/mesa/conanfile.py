# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rm, rmdir
from conan.tools.gnu import PkgConfigDeps
from conan.tools.layout import basic_layout
from conan.tools.meson import Meson, MesonToolchain
from conan.tools.scm import Version
import os

required_conan_version = ">=2.1"


class MesaConan(ConanFile):
    name = "mesa"
    description = (
        "Mesa's gallium swrast/llvmpipe software rasterizer, built as "
        "classic libOSMesa.so (every pinned version) and, where the OS "
        "distribution's own build is confirmed LLVM-linked, also as a "
        "loadable DRI driver module (swrast_dri.so) -- both linked against "
        "ASWF's own pinned LLVM instead. Covers the two ways a process ends "
        "up loading Mesa's software rasterizer -- direct linking/dlopen of "
        "classic OSMesa, and libGL's LIBGL_ALWAYS_SOFTWARE DRI-driver search "
        "-- so that a process which also loads osl/openvdb/openimagedenoise "
        "never ends up with two different libLLVM SONAMEs in the same "
        "address space the way it would with the OS-provided drivers. See "
        "the README's GPU Considerations section for how to point consumers "
        "at this package's copies instead of the system ones, and for which "
        "of the two is actually needed on a given base OS."
    )
    license = "MIT"
    homepage = "https://www.mesa3d.org/"
    url = "https://gitlab.freedesktop.org/mesa/mesa"
    topics = ("opengl", "mesa", "swrast", "llvmpipe", "osmesa", "software-rendering")

    package_type = "shared-library"
    settings = "os", "arch", "compiler", "build_type"

    @property
    def _build_dri(self):
        # The EL8 pin (23.1.4) matches a system swrast_dri.so confirmed
        # LLVM-linked (readelf -d: NEEDED libLLVM-17.so) -- a real conflict
        # risk, so this package builds its own. The EL9 pin (25.0.7) matches
        # a system swrast_dri.so confirmed to have no LLVM dependency at all
        # (same check), so there's nothing to fix there and this recipe
        # skips the extra EGL/shared-glapi build-graph scaffolding that the
        # DRI target needs (see generate()/package()) -- osmesa stays the
        # only target built. See the README's GPU Considerations section.
        return Version(self.version) < "24"

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        basic_layout(self, src_folder="src")

    def requirements(self):
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires("libdrm/2.4.120")
        self.requires(self.conf.get("user.aswf:mesa_clang_ref", check_type=str))

    def build_requirements(self):
        self.tool_requires(self.conf.get("user.aswf:mesa_clang_ref", check_type=str))
        self.tool_requires("meson/[>=1.4.0 <2]")
        # Mesa's own meson.build needs the Python "mako" module (for codegen
        # templates) available to whatever interpreter it finds -- not
        # upstream's own requirement, this project just has no other
        # reliable way to guarantee it's there (the system python3 differs
        # by distro -- EL8 is aliased to 3.11, EL9 stays on its older
        # default 3.9 -- and isn't guaranteed to have pip at all).
        self.tool_requires("cpython/[>=3.0.0]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        PkgConfigDeps(self).generate()
        tc = MesonToolchain(self, backend="ninja")
        options = {
            "auto_features": "disabled",
            "gallium-drivers": "swrast",
            "glx": "disabled",
            "gbm": "disabled",
            "platforms": [],
            "vulkan-drivers": [],
            "osmesa": True,
            "llvm": "enabled",
            "shared-llvm": "enabled",
        }
        if self._build_dri:
            # The gallium DRI target (swrast_dri.so) only gets instantiated
            # as a real build target when EGL is enabled -- glx=disabled
            # alone leaves with_dri resolved true in the config summary but
            # produces no actual *_dri.so target (verified directly against
            # mesa-23.1.4's meson introspection output, not just its text
            # summary). EGL in turn requires shared-glapi. This drags in
            # libEGL.so/headers as build-graph scaffolding; package() strips
            # all of it except libglapi.so, a real runtime dependency of
            # swrast_dri.so (confirmed via its DT_NEEDED entries) once
            # shared-glapi is on (see src/gallium/targets/osmesa/meson.build:
            # without it, osmesa statically embeds its own glapi instead and
            # doesn't need this at all, which is why the EL9-only branch
            # above skips all of this).
            options.update({
                "egl": "enabled",
                "egl-native-platform": "surfaceless",
                "shared-glapi": "enabled",
            })
        tc.project_options.update(options)
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        # Mesa's meson.build needs mako/pyyaml importable by whichever
        # python3 it finds on PATH -- which is this cpython tool_require's
        # own (its package already provides a real "python3" from CPython's
        # own native install, found correctly via the usual tool_requires
        # PATH without any extra help). Mesa 23.1.4 (2023-2026) also still
        # imports the stdlib "distutils" module to version-check mako;
        # that module was removed in Python 3.12, which our pinned cpython
        # already is. setuptools ships a compatibility shim
        # (_distutils_hack, via a .pth file) that makes "import distutils"
        # resolve to its own vendored copy -- installing it is the
        # standard workaround for this exact "No module named 'distutils'"
        # error, not something specific to this recipe.
        python3_exe = os.path.join(self.dependencies.build["cpython"].package_folder, "bin", "python3")
        self.run(f"{python3_exe} -m pip install --quiet mako pyyaml setuptools")
        meson = Meson(self)
        meson.configure()
        meson.build()

    def package(self):
        copy(self, "docs/license.rst", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
        meson = Meson(self)
        meson.install()
        # Strip the EGL build-graph scaffolding (see generate()) down to just
        # swrast_dri.so, kms_swrast_dri.so, libOSMesa.so*, and -- when the
        # DRI target was built -- libglapi.so*, which it needs at runtime.
        rmdir(self, os.path.join(self.package_folder, "include"))
        rmdir(self, os.path.join(self.package_folder, "share"))
        rm(self, "*.pc", self.package_folder, recursive=True)
        rm(self, "libEGL.so*", self.package_folder, recursive=True)

    def package_info(self):
        # Nothing to requires() against: both artifacts are either a
        # runtime-loaded driver module (swrast_dri.so) or something a
        # consumer would dlopen/LD_LIBRARY_PATH its way to rather than link
        # through Conan (libOSMesa.so) -- see the README's GPU Considerations
        # section. This package's cpp_info is deliberately empty; it only
        # exists in the Conan graph (see openusd's conanfile.py requirements())
        # so aswf_deploy copies its package_folder into /usr/local of every
        # image that already pulls in openusd.
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
