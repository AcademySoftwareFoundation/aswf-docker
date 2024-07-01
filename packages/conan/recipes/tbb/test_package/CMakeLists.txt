cmake_minimum_required(VERSION 3.12)
project(testpackage_exe LANGUAGES CXX)

find_package(TBB REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)

target_include_directories(${PROJECT_NAME} PRIVATE ${Tbb_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} tbb::tbb)
