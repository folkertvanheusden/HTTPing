cmake_minimum_required(VERSION 3.12)

project(httping LANGUAGES C VERSION "4.4.0")

# Create compile_commands.json file
set(CMAKE_EXPORT_COMPILE_COMMANDS 1)

if(NOT PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  # Git auto-ignore out-of-source build directory
  file(GENERATE OUTPUT .gitignore CONTENT "*")
endif()

option(USE_TUI "Enable text user interface" OFF)
option(USE_FFTW3 "Enable FFTW3 backend (depedns on USE_TUI)" OFF)
option(USE_SSL "Enable SSL support" OFF)
option(USE_GETTEXT "Enable interantionalization" OFF)

add_compile_options(-Wall -pedantic -Wextra)
add_compile_options(-Werror=unused-label)
add_compile_options(-Werror=unused-parameter)
add_compile_options(-Werror=strict-prototypes)

set(SOURCES
  colors.c
  cookies.c
  error.c
  gen.c
  help.c
  http.c
  io.c
  kalman.c
  main.c
  res.c
  socks5.c
  tcp.c
  utils.c
)

if(USE_SSL)
  set(SOURCES ${SOURCES} mssl.c)
endif()

if(USE_TUI)
  set(SOURCES ${SOURCES} nc.c)
  if(USE_FFTW3)
    set(SOURCES ${SOURCES} fft.c)
  endif()
endif()

add_executable(httping ${SOURCES})

target_link_libraries(httping m)

if(USE_GETTEXT)
  find_package(Gettext REQUIRED)

  find_package(Intl REQUIRED)
  target_link_libraries(httping Intl::Intl)
endif()

set(CMAKE_BUILD_TYPE Debug)

include(FindPkgConfig)

if(USE_TUI)
  pkg_check_modules(NCURSES REQUIRED ncurses)
  target_link_libraries(httping ${NCURSES_LIBRARIES})
  target_include_directories(httping PUBLIC ${NCURSES_INCLUDE_DIRS})
  target_compile_options(httping PUBLIC ${NCURSES_CFLAGS_OTHER})

  if(USE_FFTW3)
    pkg_check_modules(FFTW3 REQUIRED fftw3)
    target_link_libraries(httping ${FFTW3_LIBRARIES})
    target_include_directories(httping PUBLIC ${FFTW3_INCLUDE_DIRS})
    target_link_directories(httping PUBLIC ${FFTW3_LIBDIR})
    target_compile_options(httping PUBLIC ${FFTW3_CFLAGS_OTHER})
  endif()
endif()

if(USE_SSL)
  find_package(OpenSSL REQUIRED)
  target_link_libraries(httping OpenSSL::SSL OpenSSL::Crypto)
endif()

include(GNUInstallDirs)

if(USE_GETTEXT)
  add_subdirectory(po)
endif()

configure_file(config.h.in config.h)
target_include_directories(httping PUBLIC "${PROJECT_BINARY_DIR}")

install(TARGETS httping DESTINATION bin)
install(FILES README.md LICENSE plot-json.py DESTINATION ${CMAKE_INSTALL_DOCDIR})
install(FILES httping.1 DESTINATION ${CMAKE_INSTALL_MANDIR})

# setup summary
message(STATUS "CMake version: ${CMAKE_VERSION}")
message(STATUS "Use SSL: ${USE_SSL}")
message(STATUS "Use TUI: ${USE_TUI}")
if(USE_TUI AND USE_FFTW3)
  message(STATUS "Use FFTW3: ON")
else()
  message(STATUS "Use FFTW3: OFF")
endif()
message(STATUS "Use gettext: ${USE_GETTEXT}")
