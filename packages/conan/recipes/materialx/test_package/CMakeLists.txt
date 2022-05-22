cmake_minimum_required(VERSION 3.12)
project(testmaterialx_exe LANGUAGES CXX)

message("CMAKE_MODULE_PATH: $ENV{CMAKE_MODULE_PATH}")

find_package(materialx REQUIRED)

add_executable(${PROJECT_NAME} testmaterialx.cpp)

target_include_directories(${PROJECT_NAME} PRIVATE ${MaterialX_INCLUDE_DIRS})
message("MATERIALX: ${MaterialX_INCLUDE_DIRS}")
target_link_libraries(${PROJECT_NAME} materialx::materialx)
