if (CMAKE_VERSION VERSION_LESS 3.10.0)
    message(FATAL_ERROR "Python requires CMake 3.10+")
endif()

set(_requested_components ${Python_FIND_COMPONENTS})
if (NOT Python_FIND_COMPONENTS)
    set(_requested_components Interpreter)
endif()


set(_supported_components Interpreter Development)
foreach(_component ${_requested_components})
    if (NOT "${_component}" IN_LIST _supported_components)
        set(Python_FOUND False)
        set(Python_NOT_FOUND_MESSAGE "Unsupported component: ${_component}. Supported components: ${_supported_components}")
    endif()
    include("${CMAKE_CURRENT_LIST_DIR}/Python_${_component}Targets.cmake")
endforeach()


if (Development IN_LIST _requested_components)
    include("${CMAKE_CURRENT_LIST_DIR}/Python_Macros.cmake")
endif()