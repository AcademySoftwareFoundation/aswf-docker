from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools.files import (
    apply_conandata_patches,
    collect_libs,
    copy,
    export_conandata_patches,
    get,
    replace_in_file,
    rm,
    rmdir,
)
from conan.tools.layout import basic_layout
from conan.tools.scm import Version
from conans import tools
import os


required_conan_version = ">=1.52.0"


class PyBind11Conan(ConanFile):
    name = "pybind11"
    description = "Seamless operability between C++11 and Python"
    topics = "pybind11", "python", "binding"
    homepage = "https://github.com/pybind/pybind11"
    license = "BSD-3-Clause"
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def requirements(self):
        self.requires(
            f"python/{os.environ['ASWF_PYTHON_VERSION']}@{self.user}/{self.channel}"
        )

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        basic_layout(self, src_folder="src")
        # We want DSOs in lib64
        self.cpp.package.libdirs = ["lib64"]

    def source(self):
        get(
            self,
            **self.conan_data["sources"][self.version],
            destination=self.source_folder,
            strip_root=True,
        )

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["PYBIND11_INSTALL"] = True
        tc.variables["PYBIND11_TEST"] = False
        # FIXME: does this belong here?
        tc.variables["PYBIND11_CMAKECONFIG_INSTALL_DIR"] = os.path.join(
            "lib64", "cmake", "pybind11"
        )
        tc.variables["PYBIND11_PYTHON_VERSION"] = os.environ["ASWF_PYTHON_VERSION"]
        # FIXME
        # tc.variables["PYBIND11_FINDPYTHON"] = "ON"
        tc.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(
            self,
            "LICENSE",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses", self.name),
        )
        cmake = CMake(self)
        cmake.install()
        # Don't remove cmake files for standalone cmake use
        # for filename in ["pybind11Targets.cmake", "pybind11Config.cmake", "pybind11ConfigVersion.cmake"]:
        #   rm(self, filename, os.path.join(self.package_folder, "lib64", "cmake", "pybind11"))

        rmdir(self, os.path.join(self.package_folder, "share"))

        checked_target = "lto" if self.version < Version("2.11.0") else "pybind11"

        # FIXME Don't mess with cmake files?
        replace_in_file(
            self,
            os.path.join(
                self.package_folder,
                "lib64",
                "cmake",
                "pybind11",
                "pybind11Common.cmake",
            ),
            f"if(TARGET pybind11::{checked_target})",
            "if(FALSE)",
        )
        # FIXME: do we really want to not add_library()?
        # replace_in_file(self, os.path.join(self.package_folder, "lib64", "cmake", "pybind11", "pybind11Common.cmake"),
        #                     "add_library(",
        #                     "# add_library(")
        # FIXME? This should not be needed, CMake function names are case insensitive
        # replace_in_file(self, os.path.join(self.package_folder, "lib64", "cmake", "pybind11", "pybind11NewTools.cmake"),
        #                     "python_add_library(",
        #                     "Python_add_library(")
        # replace_in_file(self, os.path.join(self.package_folder, "lib64", "cmake", "pybind11", "pybind11NewTools.cmake"),
        #                     "Development.Module OPTIONAL_COMPONENTS Development.Embed",
        #                     "Development")

    def package_id(self):
        self.info.clear()

    def package_info(self):
        cmake_base_path = os.path.join("lib64", "cmake", "pybind11")
        self.cpp_info.set_property("cmake_target_name", "pybind11_all_do_not_use")
        self.cpp_info.components["headers"].includedirs = ["include"]
        self.cpp_info.components["pybind11_"].set_property(
            "cmake_target_name", "pybind11::pybind11"
        )
        self.cpp_info.components["pybind11_"].set_property(
            "cmake_module_file_name", "pybind11"
        )
        self.cpp_info.components["pybind11_"].names["cmake_find_package"] = "pybind11"
        self.cpp_info.components["pybind11_"].builddirs = [cmake_base_path]
        self.cpp_info.components["pybind11_"].requires = ["headers"]
        cmake_file = os.path.join(cmake_base_path, "pybind11Common.cmake")
        self.cpp_info.set_property("cmake_build_modules", [cmake_file])
        for generator in ["cmake_find_package", "cmake_find_package_multi"]:
            self.cpp_info.components["pybind11_"].build_modules[generator].append(
                cmake_file
            )
        self.cpp_info.components["embed"].requires = ["pybind11_"]
        self.cpp_info.components["module"].requires = ["pybind11_"]
        self.cpp_info.components["python_link_helper"].requires = ["pybind11_"]
        self.cpp_info.components["windows_extras"].requires = ["pybind11_"]
        self.cpp_info.components["lto"].requires = ["pybind11_"]
        self.cpp_info.components["thin_lto"].requires = ["pybind11_"]
        self.cpp_info.components["opt_size"].requires = ["pybind11_"]
        self.cpp_info.components["python2_no_register"].requires = ["pybind11_"]

        self.env_info.CMAKE_PREFIX_PATH.append(
            os.path.join(self.package_folder, "lib64", "cmake")
        )

    def deploy(self):
        self.copy("*", symlinks=True)
