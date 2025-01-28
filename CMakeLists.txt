cmake_minimum_required(VERSION 3.9)

add_compile_options(-Wall -pedantic -Wextra)

project(httping LANGUAGES C)

# Create compile_commands.json file
set(CMAKE_EXPORT_COMPILE_COMMANDS 1)

file (STRINGS "version" VERSION)
add_definitions(-DVERSION=\"${VERSION}\")

add_definitions(-DLOCALEDIR=\"/usr/local/share/locale\")

set(SOURCES  colors.c cookies.c error.c fft.c gen.c help.c http.c io.c kalman.c main.c mssl.c nc.c res.c socks5.c tcp.c utils.c)
add_executable(httping ${SOURCES})

target_link_libraries(httping m)

find_package(Intl REQUIRED)
target_link_libraries(httping Intl::Intl)

if (USE_GETTEXT)
find_package(Gettext REQUIRED)
endif()

set(CMAKE_BUILD_TYPE Debug)

include(FindPkgConfig)

if (USE_TUI)
pkg_check_modules(NCURSES ncurses)
target_link_libraries(httping ${NCURSES_LIBRARIES})
target_include_directories(httping PUBLIC ${NCURSES_INCLUDE_DIRS})
target_compile_options(httping PUBLIC ${NCURSES_CFLAGS_OTHER})

pkg_check_modules(FFTW3 fftw3)
target_link_libraries(httping ${FFTW3_LIBRARIES})
target_include_directories(httping PUBLIC ${FFTW3_INCLUDE_DIRS})
target_compile_options(httping PUBLIC ${FFTW3_CFLAGS_OTHER})
endif ()

find_package(OpenSSL REQUIRED)
target_link_libraries(httping OpenSSL::SSL OpenSSL::Crypto)

include(GNUInstallDirs)

if (USE_GETTEXT)
add_definitions(-DUSE_GETTEXT=1)

FIND_PROGRAM(GETTEXT_MSGFMT_EXECUTABLE msgfmt)

IF(NOT GETTEXT_MSGFMT_EXECUTABLE)
    MESSAGE("------ NOTE: msgfmt not found. Translations will *not* be installed ------")
ELSE(NOT GETTEXT_MSGFMT_EXECUTABLE)

	SET(catalogname httping)

  FILE(GLOB PO_FILES *.po)
  SET(GMO_FILES)

  FOREACH(_poFile ${PO_FILES})
    GET_FILENAME_COMPONENT(_poFileName ${_poFile} NAME)
    STRING(REGEX REPLACE "^${catalogname}_?" "" _langCode ${_poFileName} )
    STRING(REGEX REPLACE "\\.po$" "" _langCode ${_langCode} )

    IF( _langCode )
      GET_FILENAME_COMPONENT(_lang ${_poFile} NAME_WE)
      SET(_gmoFile ${CMAKE_CURRENT_BINARY_DIR}/${_lang}.gmo)

      ADD_CUSTOM_COMMAND(OUTPUT ${_gmoFile}
        COMMAND ${GETTEXT_MSGFMT_EXECUTABLE} --check -o ${_gmoFile} ${_poFile}
        DEPENDS ${_poFile})
      INSTALL(FILES ${_gmoFile} DESTINATION ${CMAKE_INSTALL_LOCALEDIR}/${_langCode}/LC_MESSAGES/ RENAME ${catalogname}.mo)
      LIST(APPEND GMO_FILES ${_gmoFile})
    ENDIF( _langCode )

  ENDFOREACH(_poFile ${PO_FILES})

  ADD_CUSTOM_TARGET(translations ALL DEPENDS ${GMO_FILES})

ENDIF(NOT GETTEXT_MSGFMT_EXECUTABLE)
endif ()





configure_file(config.h.in config.h)
target_include_directories(httping PUBLIC "${PROJECT_BINARY_DIR}")

install(TARGETS httping DESTINATION bin)
install(FILES README.md LICENSE plot-json.py DESTINATION ${CMAKE_INSTALL_DOCDIR})
install(FILES httping.1 DESTINATION ${CMAKE_INSTALL_MANDIR})
if (USE_GETTEXT)
	#install(FILES ${CMAKE_CURRENT_BINARY_DIR}/nl.mo DESTINATION ${CMAKE_INSTALL_LOCALEDIR})
	#install(FILES ${CMAKE_CURRENT_BINARY_DIR}/ru.mo DESTINATION ${CMAKE_INSTALL_LOCALEDIR})
endif ()
