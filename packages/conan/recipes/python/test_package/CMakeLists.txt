cmake_minimum_required(VERSION 3.1)
project(testpy_exe C)

find_package(Python COMPONENTS Interpreter Development)

add_executable(${PROJECT_NAME} testpy${Python_VERSION_MAJOR}.c)

target_include_directories(${PROJECT_NAME} PRIVATE ${Python_INCLUDE_DIRS})

target_link_libraries(${PROJECT_NAME} ${Python_LIBRARIES})
