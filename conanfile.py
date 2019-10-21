import os
from conans import ConanFile, tools
from packaging import version


class ConanFileInst(ConanFile):
    name = "arm-none-eabi-gcc_installer"
    description = "creates arm-none-eabi-gcc binaries package"
    version = "0.1"
    license = "MIT"
    url = "https://github.com/pepe82sh/conan-arm-none-eabi-gcc-installer"
    settings = {"os_build": ["Windows", "Linux", "Macos"],
                "compiler": {"gcc": {"version": ["5.4", "6.2", "6.3", "7.2", "7.3", "8.2"]}}}

    arm_common_path = "https://developer.arm.com/-/media/Files/downloads/gnu-rm"

    version_path_filename_map = {
        "8.2": (arm_common_path + "/8-2018q4", "gcc-arm-none-eabi-8-2018-q4-major-"),
        "7.3": (arm_common_path + "/7-2018q2", "gcc-arm-none-eabi-7-2018-q2-update-"),
        "7.2": (arm_common_path + "/7-2017q4", "gcc-arm-none-eabi-7-2017-q4-major-"),
        "6.3": (arm_common_path + "/6_1-2017q2", "gcc-arm-none-eabi-6-2017-q2-update-"),
        "6.2": (arm_common_path + "/6-2016q4", "gcc-arm-none-eabi-6_2-2016q4-20161216-"),
        "5.4": (arm_common_path + "/5_4-2016q3", "gcc-arm-none-eabi-5_4-2016q3-20160926-"),
    }

    filename_os_part_map = {
        "Windows": ("win32", "zip"),
        "Linux": ("linux", "tar.bz2"),
        "Macos": ("mac", "tar.bz2")
    }

    filename_os_part_map_pre_6_3 = {
        "Windows": ("win32-zip", "zip"),
        "Linux": ("linux", "tar.bz2"),
        "Macos": ("mac", "tar.bz2")
    }
    build_policy = "missing"
    short_paths = True

    def get_path_filename_ext(self):
        (path, filename) = self.version_path_filename_map[str(self.settings.compiler.version)]
        (filename_os_part, ext) = self.filename_os_part_map[str(self.settings.os_build)]
        if version.parse(self.settings.compiler.version) < version.parse("6.3"):
            (filename_os_part, ext) = self.filename_os_part_map_pre_6_3[str(self.settings.os_build)]
        filename += filename_os_part
        return path, filename, ext

    def source(self):
        # toolchain
        self.run("git clone https://github.com/vpetrigo/arm-cmake-toolchains.git")
        # compiler
        (path, filename, ext) = self.get_path_filename_ext()
        url = "%s/%s.%s" % (path, filename, ext)
        dest_file = "file.%s" % ext
        self.output.info("Downloading: %s" % url)
        tools.download(url, dest_file)
        tools.unzip(dest_file, destination=filename)
        # utils helper
        with open("arm-none-eabi-utils.cmake", "w+") as file:
            file.write("include(${CMAKE_CURRENT_LIST_DIR}/arm-cmake-toolchains/utils.cmake)")

    def package(self):
        (_, filename, _) = self.get_path_filename_ext()
        extracted_dirs = os.listdir(filename)
        if len(extracted_dirs) == 1:
            files_path = os.path.join(filename, extracted_dirs[0])
        else:
            files_path = filename
        self.copy("*", dst="gcc-arm-none-eabi", src=files_path)
        self.copy("*", dst="arm-cmake-toolchains", src="arm-cmake-toolchains")
        self.copy("arm-none-eabi-utils.cmake")

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "gcc-arm-none-eabi", "bin"))
        self.env_info.CONAN_CMAKE_TOOLCHAIN_FILE = os.path.join(self.package_folder, "arm-cmake-toolchains",
                                                                "arm-gcc-toolchain.cmake")
