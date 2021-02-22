# A simple SFML Cmake Boilerplate 
## Features
 - uses CMake for more modern and easier building
 - links SFML dynamically
 - works great with VSCode
 - tested on Ubuntu & GNU GCC
 - GoogleTest for testing (I recommend TestMate in VSCode)


## How to run
### in console
when in SFML_BOILERPLATE
- `mkdir build`
- `cd build`
- `cmake ..`
- `make`
- `./output` to run executable

### in VSCode
- Install CMake & CMake Tools plugins.
- turn on Intellisense
- build for specific targets using built-in button
- run target (tests or executable)


## Todo
- documentation generation
- CI/CD Pipeline (Travis?, Github Actions?)
- moving resources during build (sprites etc.)
- option to statically link libraries
- platform specific changes
