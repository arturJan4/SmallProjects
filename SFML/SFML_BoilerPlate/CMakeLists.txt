cmake_minimum_required(VERSION 3.16.3)
project(Game1 VERSION 0.1.0)    # change project name

# TODO
# I think it works 
# but it might break!


# ============= variables =============
set(This output)                        # output - program executable
set(CMAKE_CXX_STANDARD 17)              # C++ standard
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "-g -W -pedantic")  # flags

# sets logic as shared between testing library and main program executable
set(SOURCES src/geometry.cpp)
add_library(logic ${SOURCES})           

set(SOURCES_MAIN src/main.cpp)
add_executable(${This} ${SOURCES_MAIN})

include_directories(src)    # for Intellisense


# ============= tests & GoogleTest- downloading from remote repo =============
enable_testing()
add_subdirectory(tests) # ./tests/ has its own CMake

# https://github.com/google/googletest/tree/master/googletest#incorporating-into-an-existing-cmake-project
# Download and unpack googletest at configure time
configure_file(CMakeLists.txt.in googletest-download/CMakeLists.txt)
execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "CMake step for googletest failed: ${result}")
endif()
execute_process(COMMAND ${CMAKE_COMMAND} --build .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "Build step for googletest failed: ${result}")
endif()

# Prevent overriding the parent project's compiler/linker
# settings on Windows
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# Add googletest directly to our build. This defines
# the gtest and gtest_main targets.
add_subdirectory(${CMAKE_CURRENT_BINARY_DIR}/googletest-src
                 ${CMAKE_CURRENT_BINARY_DIR}/googletest-build
                 EXCLUDE_FROM_ALL)

# ============= sfml =============
find_package(SFML 2.5 COMPONENTS graphics audio REQUIRED)   # add more components if needed
target_link_libraries(${This} PRIVATE sfml-graphics sfml-audio)     # add here also

# target_link_libraries(${This} logic)                        

# cpack
set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)