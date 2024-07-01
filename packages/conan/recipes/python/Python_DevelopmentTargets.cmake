unset(_python_install_prefix)
# CMake modules installed in {platlibdir}/cmake/python need 3 levels up to find bin
get_filename_component(_python_install_prefix "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)
{% if os == "Macos" %}
set(Python_INCLUDE_DIRS "${_python_install_prefix}/Python.framework/Versions/{{version_major}}.{{version_minor}}/Headers")
set(Python_LIBRARIES "${_python_install_prefix}/Python.framework/Versions/{{version_major}}.{{version_minor}}/Python")
{% elif os == "Windows" %}
set(Python_INCLUDE_DIRS "${_python_install_prefix}/include")
set(Python_LIBRARIES "${_python_install_prefix}/libs/python{{version_major}}{{version_minor}}{{ '_d' if bt == 'Debug' else ''}}.lib")
{% else %}
set(Python_INCLUDE_DIRS "${_python_install_prefix}/include/python{{abi_suffix}}")
set(Python_LIBRARIES "${_python_install_prefix}/lib64/libpython{{abi_suffix}}.so")
{% endif %}
if (NOT TARGET Python::Python)
    add_library(Python::Python SHARED IMPORTED)
    set_target_properties(Python::Python
        PROPERTIES
{% if os != "Windows" %}
            IMPORTED_LOCATION "${Python_LIBRARIES}"
{% else %}
            IMPORTED_LOCATION "${_python_install_prefix}/python{{version_major}}{{version_minor}}{{ '_d' if bt == 'Debug' else ''}}.dll"
            IMPORTED_IMPLIB "${Python_LIBRARIES}"
{% endif %}
            INTERFACE_INCLUDE_DIRECTORIES "${Python_INCLUDE_DIRS}"
{% if os == "Macos" %}
            FRAMEWORK 1
            FRAMEWORK_VERSION {{version_major}}.{{version_minor}}.{{version_patch}}
{% endif %}
    )
endif()

if (NOT TARGET Python::Module)
{% if os == "Windows" %}
    add_library(Python::Module SHARED IMPORTED)
    set_target_properties(Python::Module
        PROPERTIES
            IMPORTED_LOCATION "${_python_install_prefix}/python{{version_major}}{{version_minor}}{{ '_d' if bt == 'Debug' else ''}}.dll"
            IMPORTED_IMPLIB "${Python_LIBRARIES}"
            INTERFACE_INCLUDE_DIRECTORIES "${Python_INCLUDE_DIRS}"
    )
{% else %}
    add_library(Python::Module INTERFACE IMPORTED)
    set_target_properties(Python::Module
        PROPERTIES
            INTERFACE_INCLUDE_DIRECTORIES "${Python_INCLUDE_DIRS}"
            {{ 'INTERFACE_LINK_OPTIONS "LINKER:-undefined,dynamic_lookup"' if os == 'Macos' else '' }}
    )
{% endif %}
endif()

unset(_python_install_prefix)
