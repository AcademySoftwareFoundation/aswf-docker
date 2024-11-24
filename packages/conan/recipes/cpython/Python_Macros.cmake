function(Python_ADD_LIBRARY name)
    cmake_parse_arguments(PARSE_ARGV 1 PYTHON_ADD_LIBRARY "STATIC;SHARED;MODULE" "" "")

    if (PYTHON_ADD_LIBRARY_STATIC)
        set(type STATIC)
    elseif (PYTHON_ADD_LIBRARY_SHARED)
        set(type SHARED)
    else()
        set(type MODULE)
    endif()

    add_library(${name} ${type} ${PYTHON_ADD_LIBRARY_UNPARSED_ARGUMENTS})

    get_property(type TARGET ${name} PROPERTY TYPE)

    if (type STREQUAL "MODULE_LIBRARY")
        target_link_libraries(${name} PRIVATE Python::Module)
        set_target_properties(${name}
            PROPERTIES
                PREFIX ""{% if os == "Windows" %}
                SUFFIX ".pyd"
                DEBUG_POSTFIX "_d"{% endif %}
        )
    else()
        target_link_libraries(${name} PRIVATE Python::Python)
    endif()
endfunction()