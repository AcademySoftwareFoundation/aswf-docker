from conans import ConanFile, CMake, tools
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch", "python"
    generators = "cmake", "cmake_find_package"

    def build(self):
        cmake = CMake(self)
        cmake.definitions["PYTHON_EXECUTABLE"] = os.path.join(
            self.deps_cpp_info["python"].bin_paths[0],
            self.deps_user_info["python"].python_interp,
        )
        with tools.environment_append(tools.RunEnvironment(self).vars):
            cmake.configure()
            cmake.build(args=["--", "VERBOSE=1"])

    def test(self):
        if not tools.cross_building(self.settings):
            with tools.environment_append({"PYTHONPATH": "lib"}):
                self.run(
                    "{} {}".format(
                        self.deps_user_info["python"].python_interp,
                        os.path.join(self.source_folder, "test.py"),
                    ),
                    run_environment=True,
                )
