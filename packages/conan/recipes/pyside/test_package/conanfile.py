from conans import ConanFile
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch", "python"
    generators = "cmake", "cmake_find_package"

    def build(self):
        pass

    def test(self):
        self.run(
            "{} {}".format(
                self.deps_user_info["python"].python_interp,
                os.path.join(self.source_folder, "test.py"),
            ),
            run_environment=True,
        )
