# Copyright (c) Contributors to the OpenFX Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: BSD 3-Clause
#
# This conanfile.py comes from the OpenFX project itself until it gets accepted
# into the Conan Center Index.
#
# From: https://github.com/AcademySoftwareFoundation/openfx/blob/158c8b69d9a2016755696138e027fdfd71bab552/conanfile.py


from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, collect_libs, get
import os

required_conan_version = ">=1.59.0"

class openfx(ConanFile):
	name = "openfx"
	# version = "1.4.0" # ASWF: version comes from environment
	license = "BSD-3-Clause"
	url = "https://github.com/AcademySoftwareFoundation/openfx"
	description = "OpenFX image processing plug-in standard"
	
	exports_sources = (
		"cmake/*",
		"Examples/*",
		"HostSupport/*",
		"include/*",
		"scripts/*",
		"Support/*",
		"CMakeLists.txt",
		"LICENSE",
		"README.md",
		"INSTALL.md"
	)

	settings = "os", "arch", "compiler", "build_type"
	options = {"use_opencl": [True, False]}
	default_options = {
		"expat/*:shared": True,
                "use_opencl": True,            # ASWF: build with OpenCL support
                "spdlog/*:header_only": True,
                "fmt/*:header_only": False     # ASWF: our fmt is not build header_only
	}

	def export_sources(self):
		export_conandata_patches(self)
	
	def requirements(self):
		if self.options.use_opencl: # for OpenCL examples
			self.requires("opencl-icd-loader/2023.12.14")
			self.requires("opencl-headers/2023.12.14")
		self.requires("opengl/system") # for OpenGL examples
		self.requires("expat/2.4.8") # for HostSupport
		self.requires("cimg/3.3.2") # to draw text into images
		self.requires("spdlog/1.13.0") # for logging

	def layout(self):
		cmake_layout(self)

	def source(self):
		get(self, **self.conan_data["sources"][self.version], strip_root=True) # ASWF: download sources

	def generate(self):
		deps = CMakeDeps(self)
		deps.generate()

		tc = CMakeToolchain(self)
		tc.variables["OFX_SUPPORTS_OPENGLRENDER"] = True # ASWF: exercise OpenGL / OpenCL / CUDA dependencies
		tc.variables["OFX_SUPPORTS_OPENCLRENDER"] = True
		tc.variables["OFX_SUPPORTS_CUDARENDER"] = True
		tc.variables["BUILD_EXAMPLE_PLUGINS"] = True
		if self.settings.os == "Windows":
			tc.preprocessor_definitions["WINDOWS"] = 1
			tc.preprocessor_definitions["NOMINMAX"] = 1
		tc.generate()

	def build(self):
		apply_conandata_patches(self)
		cmake = CMake(self)
		cmake.configure()
		cmake.build()

	def package(self):
		copy(self, "cmake/*", src=self.source_folder, dst=self.package_folder)
                # ASWF: license files in project specific directory
		copy(self, "LICENSE, README.md, INSTALL.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
		copy(self, "include/*.h", src=self.source_folder, dst=self.package_folder)
		copy(self,"HostSupport/include/*.h", src=self.source_folder, dst=self.package_folder)
		copy(self,"Support/*.h", src=self.source_folder, dst=self.package_folder)
		copy(self,"Support/Plugins/include/*.h", src=self.source_folder, dst=self.package_folder)
		copy(self,"*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
		copy(self,"*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
		copy(self,"*.ofx", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)
		copy(self,"*.dll", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)
		copy(self,"*.so", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)
		copy(self,"*", src=os.path.join(self.source_folder, "Examples"), dst=os.path.join(self.package_folder, "Examples"))

	def package_info(self):
		libs = collect_libs(self)

		self.cpp_info.set_property("cmake_file_name", "openfx")
		self.cpp_info.set_property("cmake_target_name", "openfx::openfx")

		self.cpp_info.set_property("cmake_build_modules", [os.path.join("cmake", "OpenFX.cmake")])
		self.cpp_info.components["Api"].includedirs = ["include"]
		self.cpp_info.components["HostSupport"].libs = [i for i in libs if "OfxHost" in i]
		self.cpp_info.components["HostSupport"].includedirs = ["HostSupport/include"]
		self.cpp_info.components["HostSupport"].requires = ["expat::expat"]
		self.cpp_info.components["Support"].libs = [i for i in libs if "OfxSupport" in i]
		self.cpp_info.components["Support"].includedirs = ["Support/include"]
		self.cpp_info.components["Support"].requires = ["opengl::opengl"]

		if self.settings.os == "Windows":
			win_defines = ["WINDOWS", "NOMINMAX"]
			self.cpp_info.components["Api"].defines = win_defines
			self.cpp_info.components["HostSupport"].defines = win_defines
			self.cpp_info.components["Support"].defines = win_defines

		# ASWF: need to reference all dependencies to make Conan happy
		self.cpp_info.components["Examples"].requires = ["spdlog::spdlog", "cimg::cimg"]
		if self.options.use_opencl: # for OpenCL examples
			self.cpp_info.components["Examples"].requires.extend(["opencl-icd-loader::opencl-icd-loader", "opencl-headers::opencl-headers"])
