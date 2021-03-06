import subprocess
import conans


class ConanFileInst(conans.ConanFile):

    settings = "os", "compiler"
    generators = "cmake"

    def build(self):
        generator = None
        if self.settings.os == "Windows":
            generator = "MinGW Makefiles"
        cmake = conans.CMake(self, generator=generator)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def test(self):
        try:
            subprocess.check_output("arm-none-eabi-gcc --version".split())
        except FileNotFoundError:
            self.output.error("package test failed. Compiler not found!")
            raise
        else:
            self.output.success("package test passed")
