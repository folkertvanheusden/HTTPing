set(catalogname httping)

file(GLOB PO_FILES *.po)

foreach(_poFile ${PO_FILES})
  get_filename_component(_poFileName ${_poFile} NAME)
  string(REGEX REPLACE "^${catalogname}_?" "" _langCode ${_poFileName})
  string(REGEX REPLACE "\\.po$" "" _langCode ${_langCode})

  if( _langCode )
    get_filename_component(_lang ${_poFile} NAME_WE)
    set(_gmoFile ${CMAKE_CURRENT_BINARY_DIR}/${_lang}.gmo)

    gettext_process_po_files(${_langCode} ALL PO_FILES ${_poFile})
    install(
      FILES ${_gmoFile}
      DESTINATION ${CMAKE_INSTALL_LOCALEDIR}/${_langCode}/LC_MESSAGES/
      RENAME ${catalogname}.mo
    )
  endif()

endforeach()
