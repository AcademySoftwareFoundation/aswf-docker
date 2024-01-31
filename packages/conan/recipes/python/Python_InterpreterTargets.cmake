if (TARGET Python::Interpreter)
    return()
endif()

unset(_python_install_prefix)
get_filename_component(_python_install_prefix "${CMAKE_CURRENT_LIST_DIR}/../" ABSOLUTE)
{% if os == "Macos" %}
set(Python_EXECUTABLE "${_python_install_prefix}/Python.framework/Versions/{{version_major}}.{{version_minor}}/bin/python{{version_major}}.{{version_minor}}")
{% elif os == "Windows" %}
set(Python_EXECUTABLE "${_python_install_prefix}/python{{ '_d' if bt == 'Debug' else '' }}.exe")
{% else %}
set(Python_EXECUTABLE "${_python_install_prefix}/bin/python{{version_major}}.{{version_minor}}")
{% endif %}
set(Python_Interpreter_FOUND True)

add_executable(Python::Interpreter IMPORTED)
set_target_properties(Python::Interpreter PROPERTIES IMPORTED_LOCATION ${Python_EXECUTABLE})