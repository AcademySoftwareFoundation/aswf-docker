# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/7abb9ee39e6009e3dbc45043307a1098246d4ad7/recipes/boost/all/test_package/CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

if(UNIX AND NOT APPLE)
    # use RPATH instead of RUNPATH so that
    # transitive dependencies can be located
    add_link_options("LINKER:--disable-new-dtags")
endif()

include(CTest)
enable_testing()

if(BOOST_NAMESPACE)
    add_definitions("-DBOOST_NAMESPACE=${BOOST_NAMESPACE}")
endif()

if(NOT HEADER_ONLY)
    if(WITH_RANDOM)
        find_package(Boost COMPONENTS random REQUIRED)
        add_executable(random_exe random.cpp)
        target_link_libraries(random_exe PRIVATE Boost::random)
        add_test(NAME boost_random COMMAND random_exe)
    endif()

    if(WITH_REGEX)
        find_package(Boost COMPONENTS regex REQUIRED)
        add_executable(regex_exe regex.cpp)
        target_link_libraries(regex_exe PRIVATE Boost::regex)
        set_property(TARGET regex_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_regex COMMAND regex_exe)
    endif()

    if(WITH_TEST)
        find_package(Boost COMPONENTS unit_test_framework REQUIRED)
        add_executable(test_exe test.cpp)
        target_link_libraries(test_exe PRIVATE Boost::unit_test_framework)
        set_property(TARGET test_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_test COMMAND test_exe)
    endif()

    if(WITH_COROUTINE)
        find_package(Boost COMPONENTS coroutine REQUIRED)
        add_executable(coroutine_exe coroutine.cpp)
        target_link_libraries(coroutine_exe PRIVATE Boost::coroutine)
        set_property(TARGET coroutine_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME coroutine_test COMMAND coroutine_exe)
    endif()

    if(WITH_CHRONO)
        find_package(Boost COMPONENTS chrono REQUIRED)
        add_executable(chrono_exe chrono.cpp)
        target_link_libraries(chrono_exe PRIVATE Boost::chrono)
        set_property(TARGET chrono_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME chrono_test COMMAND chrono_exe)
    endif()

    if(WITH_FIBER)
        find_package(Boost COMPONENTS fiber REQUIRED)
        add_executable(fiber_exe fiber.cpp)
        target_link_libraries(fiber_exe PRIVATE Boost::fiber)
        set_property(TARGET fiber_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_fiber COMMAND fiber_exe)
    endif()

    if(WITH_JSON)
        find_package(Boost COMPONENTS json REQUIRED)
        add_executable(json_exe json.cpp)
        target_link_libraries(json_exe PRIVATE Boost::json)
        set_property(TARGET json_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_json COMMAND json_exe)
    endif()

    if(WITH_NOWIDE)
        find_package(Boost COMPONENTS nowide REQUIRED)
        add_executable(nowide_exe nowide.cpp)
        target_link_libraries(nowide_exe PRIVATE Boost::nowide)
        set_property(TARGET nowide_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_nowide COMMAND nowide_exe ${CMAKE_CURRENT_SOURCE_DIR}/conanfile.py)
    endif()

    if(WITH_LOCALE)
        find_package(Boost COMPONENTS locale REQUIRED)
        add_executable(locale_exe locale.cpp)
        target_link_libraries(locale_exe PRIVATE Boost::locale)
        set_property(TARGET locale_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_locale COMMAND locale_exe)
    endif()

    if(WITH_STACKTRACE_ADDR2LINE)
        find_package(Boost COMPONENTS stacktrace REQUIRED)
        add_executable(stacktrace_addr2line_exe stacktrace.cpp)
        target_compile_definitions(stacktrace_addr2line_exe PRIVATE TEST_STACKTRACE_IMPL=1)
        target_link_libraries(stacktrace_addr2line_exe PRIVATE Boost::stacktrace_addr2line)
        set_property(TARGET stacktrace_addr2line_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_stacktrace_addr2line COMMAND stacktrace_addr2line_exe)
    endif()

    if(WITH_STACKTRACE_BACKTRACE)
        add_executable(stacktrace_backtrace_exe stacktrace.cpp)
        target_compile_definitions(stacktrace_backtrace_exe PRIVATE TEST_STACKTRACE_IMPL=2)
        target_link_libraries(stacktrace_backtrace_exe PRIVATE Boost::stacktrace_backtrace)
        set_property(TARGET stacktrace_backtrace_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_stacktrace_backtrace COMMAND stacktrace_backtrace_exe)
    endif()

    if(WITH_STACKTRACE)
        find_package(Boost COMPONENTS stacktrace REQUIRED)

        add_executable(stacktrace_noop_exe stacktrace.cpp)
        target_compile_definitions(stacktrace_noop_exe PRIVATE TEST_STACKTRACE_IMPL=4)
        target_link_libraries(stacktrace_noop_exe PRIVATE Boost::stacktrace_noop)
        set_property(TARGET stacktrace_noop_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_stacktrace_noop COMMAND stacktrace_noop_exe)

        if(WIN32)
            add_executable(stacktrace_windbg_exe stacktrace.cpp)
            target_compile_definitions(stacktrace_windbg_exe PRIVATE TEST_STACKTRACE_IMPL=5)
            target_link_libraries(stacktrace_windbg_exe PRIVATE Boost::stacktrace_windbg)
            set_property(TARGET stacktrace_windbg_exe PROPERTY CXX_STANDARD 11)
            add_test(NAME boost_stacktrace_windbg COMMAND stacktrace_windbg_exe)

            add_executable(stacktrace_windbg_cached_exe stacktrace.cpp)
            target_compile_definitions(stacktrace_windbg_cached_exe PRIVATE TEST_STACKTRACE_IMPL=6)
            target_link_libraries(stacktrace_windbg_cached_exe PRIVATE Boost::stacktrace_windbg_cached)
            set_property(TARGET stacktrace_windbg_cached_exe PROPERTY CXX_STANDARD 11)
            add_test(NAME boost_stacktrace_windbg_cached COMMAND stacktrace_windbg_cached_exe)
        else()
            add_executable(stacktrace_basic_exe stacktrace.cpp)
            target_compile_definitions(stacktrace_basic_exe PRIVATE TEST_STACKTRACE_IMPL=3)
            target_link_libraries(stacktrace_basic_exe PRIVATE Boost::stacktrace_basic)
            set_property(TARGET stacktrace_basic_exe PROPERTY CXX_STANDARD 11)
            add_test(NAME boost_stacktrace_basic COMMAND stacktrace_basic_exe)
        endif()
    endif()

    if (WITH_PROCESS)
        find_package(Boost COMPONENTS process REQUIRED)
        add_executable(process_exe process.cpp)
        target_link_libraries(process_exe PRIVATE Boost::process)
        set_property(TARGET process_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_process COMMAND process_exe)
    endif()

    if(WITH_PYTHON)
        find_package(Boost COMPONENTS python REQUIRED)
        add_library(hello_ext MODULE python.cpp)
        set_property(TARGET hello_ext PROPERTY PREFIX "")

        find_package(Python3 ${PYTHON_VERSION_TO_SEARCH} COMPONENTS Interpreter Development NumPy REQUIRED)

        target_link_libraries(hello_ext PRIVATE Boost::python Python3::Python)
        if(WIN32)
            set_target_properties(hello_ext PROPERTIES SUFFIX ".pyd")
        endif()
        add_test(NAME boost_python COMMAND Python3::Interpreter "${CMAKE_CURRENT_SOURCE_DIR}/python.py")
        set_property(TEST boost_python PROPERTY ENVIRONMENT "PYTHONPATH=$<TARGET_FILE_DIR:hello_ext>")

        add_executable(numpy_exe numpy.cpp)
        target_link_libraries(numpy_exe PRIVATE Boost::numpy Python3::Python Python3::NumPy)
        add_test(NAME boost_numpy COMMAND numpy_exe)
        set_property(TEST boost_numpy PROPERTY ENVIRONMENT "PYTHONPATH=${Python_SITELIB}")
    endif()

    if(WITH_URL)
        find_package(Boost COMPONENTS url REQUIRED)
        add_executable(url_exe url.cpp)
        target_link_libraries(url_exe PRIVATE Boost::url)
        set_property(TARGET url_exe PROPERTY CXX_STANDARD 11)
        add_test(NAME boost_url COMMAND url_exe)
    endif()

endif()

# Test header-only target
find_package(Boost REQUIRED)
add_executable(lambda_exe lambda.cpp)
target_link_libraries(lambda_exe PRIVATE Boost::headers)
add_test(NAME boost_boost COMMAND lambda_exe)


