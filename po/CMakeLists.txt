add_definitions(-DUSE_GETTEXT=1)

find_program(GETTEXT_MSGFMT_EXECUTABLE msgfmt)

if(NOT GETTEXT_MSGFMT_EXECUTABLE)
  message("------ NOTE: msgfmt not found. Translations will *not* be installed ------")
else(NOT GETTEXT_MSGFMT_EXECUTABLE)

  set(catalogname httping)

  file(GLOB PO_FILES *.po)
  set(GMO_FILES)

  foreach(_poFile ${PO_FILES})
    get_filename_component(_poFileName ${_poFile} NAME)
    string(REGEX REPLACE "^${catalogname}_?" "" _langCode ${_poFileName} )
    string(REGEX REPLACE "\\.po$" "" _langCode ${_langCode} )

    if( _langCode )
      get_filename_component(_lang ${_poFile} NAME_WE)
      set(_gmoFile ${CMAKE_CURRENT_BINARY_DIR}/${_lang}.gmo)

      add_custom_command(OUTPUT ${_gmoFile}
        COMMAND ${GETTEXT_MSGFMT_EXECUTABLE} --check -o ${_gmoFile} ${_poFile}
        DEPENDS ${_poFile})
      install(FILES ${_gmoFile} DESTINATION ${CMAKE_INSTALL_LOCALEDIR}/${_langCode}/LC_MESSAGES/ RENAME ${catalogname}.mo)
      list(APPEND GMO_FILES ${_gmoFile})
    endif( _langCode )

  endforeach(_poFile ${PO_FILES})

  add_custom_target(translations ALL DEPENDS ${GMO_FILES})

endif(NOT GETTEXT_MSGFMT_EXECUTABLE)

#install(FILES ${CMAKE_CURRENT_BINARY_DIR}/nl.mo DESTINATION ${CMAKE_INSTALL_LOCALEDIR})
#install(FILES ${CMAKE_CURRENT_BINARY_DIR}/ru.mo DESTINATION ${CMAKE_INSTALL_LOCALEDIR})
