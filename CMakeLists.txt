cmake_minimum_required(VERSION 2.8.12)
project(sword_and_sorcery)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

set(SOURCES src/board_status.cpp)
# set(HEADERS include/board_status.h)

add_library(messages ${SOURCES})
set_target_properties(messages PROPERTIES CXX_STANDARD 17)
target_link_libraries(messages PUBLIC CONAN_PKG::protobuf)

target_include_directories(
    messages PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

install(
    TARGETS messages
    EXPORT messages-config
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(
    EXPORT messages-config
    NAMESPACE messages::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake)

install(
    DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
