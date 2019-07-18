cmake_minimum_required(VERSION 2.8.12)
project(sword_and_sorcery)

include(GenerateExportHeader)
include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(Protobuf REQUIRED)  # TODO: NO_CMAKE_PACKAGE_REGISTRY

# Generate protobuffers
set(PROTOBUF_GENERATE_CPP_APPEND_PATH OFF)
set(PROTO_FILES messages/layer.proto messages/board_status.proto)
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_FILES} EXPORT_MACRO MESSAGES_EXPORT)

set(SOURCES "")
foreach(PROTO ${PROTO_SRCS})
    get_filename_component(PROTO_FILE ${PROTO} NAME)
    list(APPEND SOURCES "${CMAKE_CURRENT_BINARY_DIR}/messages/${PROTO_FILE}")
    message("> ${PROTO_FILE}")
endforeach()
set_source_files_properties(${SOURCES} PROPERTIES GENERATED TRUE)
add_custom_target(protobuf_generate_cpp DEPENDS ${PROTO_FILES} ${SOURCES})  # TODO: ??

# Target
add_library(messages ${SOURCES} ${PROTO_FILES})
add_dependencies(messages protobuf_generate_cpp)
set_target_properties(messages PROPERTIES CXX_STANDARD 17)
target_link_libraries(messages PUBLIC CONAN_PKG::protobuf)
target_include_directories(messages
        PUBLIC
            $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
            $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
        )

generate_export_header(messages EXPORT_FILE_NAME ${CMAKE_CURRENT_BINARY_DIR}/include/messages_api.h)
if(MSVC)
    target_compile_options(messages PUBLIC /FI"${CMAKE_CURRENT_BINARY_DIR}/include/messages_api.h")
else()
    # GCC or Clang
    target_compile_options(messages PUBLIC -include ${CMAKE_CURRENT_BINARY_DIR}/include/messages_api.h)
endif()
