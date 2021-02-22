cmake_minimum_required(VERSION 3.16.3)

# works great with CTest integration in VSCode
# name of this target
set(This BoilerTests)

# add test files here
set(Sources geometryTests.cpp hardMathTests.cpp)

add_executable(${This} ${Sources})

# links testing with logic files (all .cpp & .hpp files except main)
target_link_libraries(${This} PUBLIC  
    gtest_main
    logic
)

add_test(
    NAME ${This}
    COMMAND ${This}
)