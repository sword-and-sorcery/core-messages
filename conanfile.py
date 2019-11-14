import os
from conans import ConanFile, CMake

class CoreMessages(ConanFile):
    name = "core-messages"
    version = "0.0"

    url = "https://github.com/sword-and-sorcery/core-messages"
    homepage = "https://sword-and-sorcery.github.io/sword-and-sorcery/"
    author = "conan.io"
    license = "MIT"
    description = "Definition of common messages across the framework"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    generators = "cmake"

    scm = {"type": "git",
           "url": "auto",
           "revision": "auto"}

    exports = "messages/*.proto"

    def requirements(self):
        self.requires("protobuf/3.9.1@bincrafters/stable")

    def build_requirements(self):
        self.build_requires("protoc_installer/3.6.1@bincrafters/stable")

    def source(self):
        # Generate protobuf messages
        input_message_folder = os.path.join(os.path.dirname(__file__), "messages")
        output_message_folder = os.path.join(self.source_folder, "messages")
        self.output.info("input_message_folder: {}".format(input_message_folder))
        self.output.info("output_message_folder: {}".format(output_message_folder))

        messages = [os.path.join(input_message_folder, it) for it in os.listdir(input_message_folder) if it.endswith(".proto")]
        command = "protoc --proto_path={}".format(input_message_folder)
        command += " --cpp_out={}".format(output_message_folder)
        command += " {}".format(" ".join(messages))
        self.run(command)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE", dst="licenses")

    def package_info(self):
        self.cpp_info.libs = ["messages",]
