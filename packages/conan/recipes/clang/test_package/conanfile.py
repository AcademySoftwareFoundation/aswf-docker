from conans import ConanFile, CMake, tools

import os.path


class LLVMCoreTestPackageConan(ConanFile):
    settings = ("os", "arch", "compiler", "build_type")
    generators = ("cmake", "cmake_find_package")

    def build(self):
        build_system = CMake(self)
        build_system.verbose = True
        build_system.configure()
        build_system.build()

    def test(self):
        test_package = not tools.cross_building(self.settings)
        if "x86" not in str(self.settings.arch).lower():
            test_package = False
        elif str(self.options["clang"].targets) not in ["all", "X86"]:
            test_package = False
        else:
            if self.options["clang"].components != "all":
                requirements = ["interpreter", "irreader", "x86codegen"]
                targets = str(self.options["clang"].components)
                if self.settings.os == "Windows":
                    requirements.append("demangle")
                if not all([target in targets for target in requirements]):
                    test_package = False

        if test_package:
            command = [
                os.path.join("bin", "test_package"),
                os.path.join(os.path.dirname(__file__), "test_function.ll"),
            ]
            self.run(command, run_environment=True)

        llvm_path = self.deps_cpp_info["clang"].rootpath
        license_path = os.path.join(llvm_path, "licenses", "clang", "LICENSE.TXT")
        assert os.path.exists(license_path)
