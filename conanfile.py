from conans import ConanFile, CMake

class CoreMessages(ConanFile):
    name = "core-messages"
    version = "0.0"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    generators = "cmake"

    scm = {"type": "git",
           "url": "auto",
           "revision": "auto"}

    def requirements(self):
        self.requires("protobuf/3.6.1@bincrafters/stable")

    def build_requirements(self):
        self.build_requires("protoc_installer/3.6.1@bincrafters/stable")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["messages",]
