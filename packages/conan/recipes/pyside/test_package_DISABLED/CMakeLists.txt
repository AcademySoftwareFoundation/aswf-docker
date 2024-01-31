cmake_minimum_required(VERSION 3.13)
project(PackageTest LANGUAGES CXX)

find_package(Python CONFIG EXACT REQUIRED COMPONENTS Interpreter Development)

message(STATUS "Python executable testing is '${Python_EXECUTABLE}'")
set(PYHOME ${CONAN_PYTHON_ROOT})
if (APPLE)
    set(PYHOME ${CONAN_PYTHON_ROOT}/Python.framework/Versions/Current)
endif()
message(STATUS "PYTHONHOME is ${PYHOME}")
message(STATUS "PYTHONPATH is $ENV{PYTHONPATH}")
if(UNIX AND NOT APPLE)
    message(STATUS "LD_LIBRARY_PATH is $ENV{LD_LIBRARY_PATH}")
endif()

enable_testing()

macro(add_python_test CASE_NAME SCRIPT_FILE)
    add_test(
        NAME ${CASE_NAME}
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMAND $<TARGET_FILE:Python::Interpreter> -s ${CMAKE_CURRENT_SOURCE_DIR}/${SCRIPT_FILE} ${ARGN}
    )

    set_tests_properties(${CASE_NAME} PROPERTIES ENVIRONMENT "PYTHONHOME=${PYHOME};PATH=${CONAN_QT_ROOT}/bin;${CONAN_PYSIDE6_ROOT}/bin;$ENV{PATH}")
endmacro()

add_python_test(basic_version_test test_version.py ${CONAN_PYSIDE_VERSION})
add_python_test(basic_qt_core_test test_qt_core.py "")
add_python_test(basic_uic_test test_uic.py ${CONAN_PYSIDE6_ROOT} ${CONAN_PYSIDE_VERSION})


find_package(PySide6 REQUIRED)
find_package(Shiboken6 REQUIRED)
find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

add_library(test_pyside SHARED test_pyside.cpp)
target_link_libraries(
    test_pyside
    PRIVATE
    PySide6::pyside6
    Shiboken6::libshiboken
    Qt::Widgets
)
