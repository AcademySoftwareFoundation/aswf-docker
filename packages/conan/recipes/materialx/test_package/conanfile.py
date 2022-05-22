from conans import ConanFile, tools, CMake
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch", "python"
    generators = "cmake_find_package_multi"

    def build(self):
        cmake = CMake(self)
        with tools.environment_append(tools.RunEnvironment(self).vars):
            cmake.configure()
            cmake.build(args=["--", "VERBOSE=1"])

    def test(self):
        self.run("./testmaterialx_exe", run_environment=True)
        self.run(
            "{} {}".format(
                self.deps_user_info["python"].python_interp,
                os.path.join(self.source_folder, "testmaterialx.py"),
            ),
            run_environment=True,
        )
