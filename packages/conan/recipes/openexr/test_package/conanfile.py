from conans import ConanFile, tools, CMake
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch", "python"

    def build(self):
        cmake = CMake(self)
        with tools.environment_append(tools.RunEnvironment(self).vars):
            self.run("echo CMAKE_PREFIX_PATH=$CMAKE_PREFIX_PATH")
            cmake.definitions["OPENEXR_LOCATION"] = os.path.dirname(
                self.deps_cpp_info["openexr"].lib_paths[0]
            )
            cmake.configure()
            cmake.build(args=["--", "VERBOSE=1"])

    def test(self):
        self.run("./testopenexr_exe", run_environment=True)
        if (
            os.environ.get("ASWF_OPENEXR_VERSION") == "2.4.0"
            and os.environ.get("ASWF_PYTHON_VERSION") == "3.7.3"
        ):
            # Known incompatibility for python3...
            return
        self.run(
            "{} {}".format(
                self.deps_user_info["python"].python_interp,
                os.path.join(self.source_folder, "testopenexr.py"),
            ),
            run_environment=True,
        )
