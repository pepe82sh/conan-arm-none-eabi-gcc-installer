import subprocess
import conans


class ConanFileInst(conans.ConanFile):

    def build(self):
        pass

    def test(self):
        try:
            subprocess.check_output("arm-none-eabi-gcc --version".split())
        except FileNotFoundError:
            self.output.error("package test failed. Compiler not found!")
            raise
        else:
            self.output.success("package test passed")
