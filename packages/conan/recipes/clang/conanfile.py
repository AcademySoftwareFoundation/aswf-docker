from conans import ConanFile, CMake, tools

import os.path
import os


class ClangConan(ConanFile):
    name = "clang"
    description = (
        "A toolkit for the construction of highly optimized compilers,"
        "optimizers, and runtime environments."
    )
    license = "Apache-2.0 WITH LLVM-exception"
    topics = ("conan", "llvm", "clang")
    homepage = "https://github.com/llvm/llvm-project/tree/master/llvm"
    url = "https://github.com/AcademySoftwareFoundation/aswf-docker"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "components": "ANY",
        "targets": "ANY",
    }
    default_options = {
        "components": "llvm;clang;clang-tools-extra;libcxx;libcxxabi;compiler-rt;lld",
        "targets": "host;NVPTX",
    }

    exports_sources = ["CMakeLists.txt", "patches/*"]
    generators = ["cmake", "cmake_find_package"]
    no_copy_source = True

    @property
    def _source_subfolder(self):
        return "source"

    def build_requirements(self):
        if tools.Version(self.version) > "11":
            self.build_requires(f"python/3.9.7@{self.user}/vfx2022")

    def configure(self):
        compiler = self.settings.compiler.value
        version = tools.Version(self.settings.compiler.version)
        if (
            tools.Version(self.version) >= "13"
            and compiler == "gcc"
            and int(version.major) == 9
        ):
            # llvm-13 fails to build (mostly unused) libc++
            # see https://www.mail-archive.com/llvm-bugs@lists.llvm.org/msg53136.html
            self.options.components.value = self.options.components.value.replace(
                "libcxx;libcxxabi;", ""
            )

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["GCC_INSTALL_PREFIX"] = os.environ["GCC_INSTALL_PREFIX"]
        cmake.definitions["LLVM_BUILD_LLVM_DYLIB"] = True
        cmake.definitions["CLANG_INCLUDE_DOCS"] = False
        cmake.definitions["LIBCXX_INCLUDE_DOCS"] = False
        cmake.definitions["LLVM_BUILD_TESTS"] = False
        cmake.definitions["LLVM_INCLUDE_TESTS"] = False
        cmake.definitions["LLVM_INCLUDE_TOOLS"] = True
        cmake.definitions["LLVM_BUILD_TOOLS"] = True
        cmake.definitions["LLVM_TOOL_LLVM_AR_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_AS_BUILD"] = True
        cmake.definitions["LLVM_TOOL_LLVM_AS_FUZZER_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_BCANALYZER_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_COV_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_CXXDUMP_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_DIS_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_EXTRACT_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_C_TEST_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_DIFF_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_GO_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_JITLISTENER_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_LTO_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_MC_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_NM_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_OBJDUMP_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_BCANALYZER_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_PROFDATA_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_RTDYLD_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_SIZE_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_SPLIT_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_STRESS_BUILD"] = False
        cmake.definitions["LLVM_TOOL_LLVM_SYMBOLIZER_BUILD"] = True
        cmake.definitions["LLVM_TOOL_LLVM_LTO_BUILD"] = False
        cmake.definitions["LLVM_INCLUDE_EXAMPLES"] = False
        cmake.definitions["CMAKE_SKIP_RPATH"] = True
        cmake.definitions["LLVM_ENABLE_PROJECTS"] = self.options.components
        cmake.definitions["LLVM_TARGETS_TO_BUILD"] = self.options.targets

        if self.settings.compiler == "Visual Studio":
            build_type = str(self.settings.build_type).upper()
            cmake.definitions[
                "LLVM_USE_CRT_{}".format(build_type)
            ] = self.settings.compiler.runtime

        return cmake

    def source(self):
        tools.get(
            f"https://github.com/llvm/llvm-project/archive/llvmorg-{self.version}.tar.gz"
        )
        os.rename(
            "llvm-project-llvmorg-{}".format(self.version), self._source_subfolder
        )

    def build(self):
        with tools.environment_append(tools.RunEnvironment(self).vars):
            cmake = self._configure_cmake()
            cmake.configure(source_folder="source/llvm")
            cmake.build()

    def package(self):
        self.copy(
            "LICENSE.TXT",
            dst="licenses",
            src=os.path.join(self._source_subfolder, "llvm"),
        )
        with tools.environment_append(tools.RunEnvironment(self).vars):
            cmake = self._configure_cmake()
            cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        try:
            self.cpp_info.libs.remove("LLVMHello")
        except ValueError:
            pass
        try:
            self.cpp_info.libs.remove("BugpointPasses")
        except ValueError:
            pass
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread", "rt", "dl", "m", "curses"]
        elif self.settings.os == "Macos":
            self.cpp_info.system_libs = ["m"]
        self.env_info.LLVM_INSTALL_DIR = self.package_folder
        self.env_info.CLANG_INSTALL_DIR = self.package_folder

    def deploy(self):
        self.copy("*")
