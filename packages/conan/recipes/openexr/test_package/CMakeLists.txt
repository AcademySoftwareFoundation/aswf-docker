cmake_minimum_required(VERSION 3.1)
project(testopenexr_exe LANGUAGES CXX)

find_package(Threads REQUIRED)
find_package(ZLIB REQUIRED)
find_package(IlmBase) # Will fail with OpenEXR 2.3
find_package(Imath) # Will fail with OpenEXR < 3.0
find_package(OpenEXR REQUIRED)

if(IlmBase_FOUND)
    set(openexr_link_lib OpenEXR::IlmImf)
else()
    set(openexr_link_lib OpenEXR::OpenEXR)
endif()


add_executable(${PROJECT_NAME} testopenexr.cpp)

target_include_directories(${PROJECT_NAME} PRIVATE ${OPENEXR_INCLUDE_DIRS})

target_link_libraries(${PROJECT_NAME} ${OPENEXR_LIBRARIES} ${openexr_link_lib})
