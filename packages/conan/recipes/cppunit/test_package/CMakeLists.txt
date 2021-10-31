cmake_minimum_required(VERSION 3.12)
project(test_package C CXX)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

add_executable(${PROJECT_NAME} test_package.cpp)
if(CPPUNIT_TEST_FIXTURE_AVAILABLE)
    target_compile_definitions(${PROJECT_NAME} "-DCPPUNIT_TEST_FIXTURE_AVAILABLE")
endif()
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 11)
