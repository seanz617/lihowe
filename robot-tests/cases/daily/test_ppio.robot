*** Settings   ***
Library    controller.test_ppio
Variables    data-center/data.py 

*** Test Cases ***
Test ppio import export delete object
  [Template]    Test ppio import export delete object ${param}
  ${PPIO_IMPORT_EXPORT_DELETE_288B}
  ${PPIO_IMPORT_EXPORT_DELETE_1K}
  ${PPIO_IMPORT_EXPORT_DELETE_16LESSM}
  ${PPIO_IMPORT_EXPORT_DELETE_16M}
  ${PPIO_IMPORT_EXPORT_DELETE_16LARGERM}
  ${PPIO_IMPORT_EXPORT_DELETE_1G}

Test ppio import put get export delete
  [Template]    Test ppio import put get export delete ${param}
  ${PPIO_PUT_GET_EXPORT_DELETE_288B}
  ${PPIO_PUT_GET_EXPORT_DELETE_1K}
  ${PPIO_PUT_GET_EXPORT_DELETE_16LESSM}
  ${PPIO_PUT_GET_EXPORT_DELETE_16M}
  ${PPIO_PUT_GET_EXPORT_DELETE_16LARGERM}
  ${PPIO_PUT_GET_EXPORT_DELETE_256M}

  ${PPIO_PUT_GET_EXPORT_DELETE_288B_BETWEEN_PPIO}
  ${PPIO_PUT_GET_EXPORT_DELETE_1K_BETWEEN_PPIO}
  ${PPIO_PUT_GET_EXPORT_DELETE_16LESSM_BETWEEN_PPIO}
  ${PPIO_PUT_GET_EXPORT_DELETE_16M_BETWEEN_PPIO}
  ${PPIO_PUT_GET_EXPORT_DELETE_16LARGERM_BETWEEN_PPIO}
  ${PPIO_PUT_GET_EXPORT_DELETE_256M_BETWEEN_PPIO}

Test ppio import put renew get export delete
  [Template]    Test ppio import put renew get export delete ${param}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_288B}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_16LESSM}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_16M}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_16LARGERM}

  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_COPY}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_COPY}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_COPY_EXPIRE}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_COPY_INC_EXPIRE}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_EXPIRE_INC_COPY}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_COPY_EXPIRE}

  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_COPY}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_COPY_EXPIRE}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_COPY_DEC_EXPIRE}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_DEC_COPY}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_EXPIRE_DEC_COPY}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_DEC_COPY_EXPIRE}

  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_COPY}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_INC_COPY}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_COPY_EXPIRE}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_COPY_INC_EXPIRE}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_EXPIRE_INC_COPY}
  ${PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_INC_COPY_EXPIRE}

*** Key Words ***
Test ppio import export delete object ${param}
  ${chunks} =    import object    ${param}[import]
  export object    ${param}[export]    ${chunks}
  delete object    ${param}[delete]    ${chunks}

Test ppio import put get export delete ${param}
  ${chunks} =    import object    ${param}[import]
  put chunks    ${param}[put]    ${chunks}
  get chunks    ${param}[get]    ${chunks}
  export object    ${param}[export]    ${chunks}
  delete chunks    ${param}[delete]    ${chunks}

Test ppio import put renew get export delete ${param}
  ${chunks} =    import object    ${param}[import]
  put chunks    ${param}[put]    ${chunks}
  renew chunks    ${param}[renew]    ${chunks}
  get chunks    ${param}[get]    ${chunks}
  export object    ${param}[export]    ${chunks}
  delete chunks    ${param}[delete]    ${chunks}
