from conans import ConanFile, CMake, tools
import os


class CpuinfoConan(ConanFile):
    name = "cpuinfo"
    version = "d5e37ad"
    description = "Keep it short"
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("conan", "libname", "logging")
    url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://github.com/original_author/original_lib"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def build_requirements(self):
        self.build_requires("glog/0.4.0@bincrafters/stable")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        git = tools.Git(folder="source_subfolder")
        git.clone("https://github.com/pytorch/cpuinfo.git", shallow=True)
        git.checkout("d5e37adf1406cf899d7d9ec1d317c47506ccb970")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CPUINFO_LIBRARY_TYPE"] = "shared" if self.options.shared else "static"
        cmake.definitions["CPUINFO_BUILD_TOOLS"] = False
        cmake.definitions["CPUINFO_BUILD_UNIT_TESTS"] = False
        cmake.definitions["CPUINFO_BUILD_MOCK_TESTS"] = False
        cmake.definitions["CPUINFO_BUILD_BENCHMARKS"] = False

        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
