cmake_minimum_required(VERSION 3.9)

add_compile_options(-Wall -pedantic -Wextra)

project(httping LANGUAGES C)
file (STRINGS "version" VERSION)
add_definitions(-DVERSION=\"${VERSION}\")

add_definitions(-DLOCALEDIR=\"/usr/share/locale\")

add_executable(
	httping
	colors.c
	cookies.c
	error.c
	fft.c
	gen.c
	help.c
	http.c
	io.c
	kalman.c
	main.c
	mssl.c
	nc.c
	res.c
	socks5.c
	tcp.c
	utils.c
)

set(CMAKE_BUILD_TYPE Debug)

target_link_libraries(httping m)

include(FindPkgConfig)

pkg_check_modules(NCURSES ncurses)
target_link_libraries(httping ${NCURSES_LIBRARIES})
target_include_directories(httping PUBLIC ${NCURSES_INCLUDE_DIRS})
target_compile_options(httping PUBLIC ${NCURSES_CFLAGS_OTHER})

pkg_check_modules(FFTW3 fftw3)
target_link_libraries(httping ${FFTW3_LIBRARIES})
target_include_directories(httping PUBLIC ${FFTW3_INCLUDE_DIRS})
target_compile_options(httping PUBLIC ${FFTW3_CFLAGS_OTHER})

pkg_check_modules(SSL libssl)
target_link_libraries(httping ${SSL_LIBRARIES})
target_include_directories(httping PUBLIC ${SSL_INCLUDE_DIRS})
target_compile_options(httping PUBLIC ${SSL_CFLAGS_OTHER})

pkg_check_modules(OPENSSL openssl)
target_link_libraries(httping ${OPENSSL_LIBRARIES})
target_include_directories(httping PUBLIC ${OPENSSL_INCLUDE_DIRS})
target_compile_options(httping PUBLIC ${OPENSSL_CFLAGS_OTHER})

execute_process (
    COMMAND bash -c "msgfmt -o nl.mo ${CMAKE_SOURCE_DIR}/nl.po"
)
execute_process (
    COMMAND bash -c "msgfmt -o ru.mo ${CMAKE_SOURCE_DIR}/ru.po"
)

configure_file(config.h.in config.h)
target_include_directories(httping PUBLIC "${PROJECT_BINARY_DIR}")
