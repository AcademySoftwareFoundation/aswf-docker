from conans import ConanFile, tools, CMake
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch", "python"

    def build(self):
        if self.deps_user_info["imath"].is_dummy:
            return
        cmake = CMake(self)
        with tools.environment_append(tools.RunEnvironment(self).vars):
            cmake.configure()
            cmake.build(args=["--", "VERBOSE=1"])

    def test(self):
        if self.deps_user_info["imath"].is_dummy:
            return
        self.run("./testimath_exe", run_environment=True)
        self.run(
            "{} {}".format(
                self.deps_user_info["python"].python_interp,
                os.path.join(self.source_folder, "testimath.py"),
            ),
            run_environment=True,
        )
