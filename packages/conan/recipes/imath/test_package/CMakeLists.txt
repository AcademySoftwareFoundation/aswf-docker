cmake_minimum_required(VERSION 3.12)
project(testimath_exe LANGUAGES CXX)

message("CMAKE_MODULE_PATH: $ENV{CMAKE_MODULE_PATH}")

find_package(Imath REQUIRED)

add_executable(${PROJECT_NAME} testimath.cpp)

target_include_directories(${PROJECT_NAME} PRIVATE ${Imath_INCLUDE_DIRS})
message("IMATH: ${Imath_INCLUDE_DIRS}")
target_link_libraries(${PROJECT_NAME} Imath::Imath)
