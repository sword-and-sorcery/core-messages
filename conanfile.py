import os
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

    def source(self):
        # Generate protobuf messages
        message_folder = os.path.join(os.path.dirname(__file__), "messages")
        self.output.info("message_folder: {}".format(message_folder))
        messages = [os.path.join(message_folder, it) for it in os.listdir(message_folder) if it.endswith(".proto")]
        command = "protoc --proto_path={}".format(message_folder)
        command += " --cpp_out={}".format(message_folder)
        command += " {}".format(" ".join(messages))
        self.run(command)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["messages",]
