cmake_minimum_required(VERSION 3.12)
project(conan_glew)

include("conanbuildinfo.cmake")
conan_basic_setup()
include(GNUInstallDirs)

add_subdirectory("source_subfolder/build/cmake")
