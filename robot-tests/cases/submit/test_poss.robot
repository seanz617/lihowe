*** Settings   ***
Library    controller.test_poss
Library    controller.test_bucket
Variables    data-center/data.py 

*** Test Cases ***
Test create bucket parameter check
  [Template]    Test create bucket parameter check ${param}
  ${POSS_CREATE_BUCKET_PARAM_CHECK_1}
  ${POSS_CREATE_BUCKET_PARAM_CHECK_2}
  ${POSS_CREATE_BUCKET_PARAM_CHECK_3}
  ${POSS_CREATE_BUCKET_PARAM_CHECK_4}
  ${POSS_CREATE_BUCKET_PARAM_CHECK_5}
  ${POSS_CREATE_BUCKET_PARAM_CHECK_6}
  ${POSS_CREATE_BUCKET_PARAM_CHECK_7}
  ${POSS_CREATE_BUCKET_PARAM_CHECK_8}

Test create same bucket
  [Template]    Test create same bucket ${param}
  ${POSS_CREATE_SAME_BUCKET}

Test delete bucket parameter check
  [Template]    Test delete bucket parameter check ${param}
  ${POSS_DELETE_BUCKET_PARAM_CHECK_1}
  ${POSS_DELETE_BUCKET_PARAM_CHECK_2}
  ${POSS_DELETE_BUCKET_PARAM_CHECK_3}

Test delete not empty bucket
  [Template]    Test delete not empty bucket ${param}
  ${POSS_DELETE_NOT_EMPTY_BUCKET}

Test create dir
  [Template]    Test create dir ${param}
  ${CREATE_DIR}

Test poss put parameter check
  [Template]   Test poss put parameter check ${param}
  ${POSS_PUT_PARAMETER_CHECK_FILE_PREPARE}
  ${POSS_PUT_PARAMETER_CHECK_FILE_NOT_FOUND}
  ${POSS_PUT_PARAMETER_CHECK_EMPTY_CHIPRICE}
  ${POSS_PUT_PARAMETER_CHECK_ZERO_CHIPRICE}
  ${POSS_PUT_PARAMETER_CHECK_NEGATIVE_CHIPRICE}
  ${POSS_PUT_PARAMETER_CHECK_STR_CHIPRICE}
  ${POSS_PUT_PARAMETER_CHECK_EMPTY_COPIES}
  ${POSS_PUT_PARAMETER_CHECK_ZERO_COPIES}
  ${POSS_PUT_PARAMETER_CHECK_NEGATIVE_COPIES}
  ${POSS_PUT_PARAMETER_CHECK_STR_COPIES}
  ${POSS_PUT_PARAMETER_CHECK_EMPTY_EXPIRES}
  ${POSS_PUT_PARAMETER_CHECK_ZERO_EXPIRES}
  ${POSS_PUT_PARAMETER_CHECK_NEGATIVE_EXPIRES}
  ${POSS_PUT_PARAMETER_CHECK_STR_EXPIRES}

Test poss get parameter check
  [Template]   Test poss get parameter check ${param}
  ${POSS_GET_PARAMETER_CHECK_LOW_CHIPRICE}
  ${POSS_GET_PARAMETER_CHECK_EMPTY_CHIPRICE}
  ${POSS_GET_PARAMETER_CHECK_ZERO_CHIPRICE}
  ${POSS_GET_PARAMETER_CHECK_NEGATIVE_CHIPRICE}
  ${POSS_GET_PARAMETER_CHECK_STR_CHIPRICE}

Test poss delete parameter check
  [Template]   Test poss delete parameter check ${param}
  ${POSS_DELETE_PARAMETER_CHECK_ERROR_BUCKET}
  ${POSS_DELETE_PARAMETER_CHECK_ERROR_KEY_1}
  ${POSS_DELETE_PARAMETER_CHECK_ERROR_KEY_2}
  ${POSS_DELETE_PARAMETER_CHECK_ERROR_KEY_3}
  ${POSS_DELETE_PARAMETER_CHECK_ERROR_KEY_4}

Test poss share parameter check
  [Template]   Test poss share parameter check ${param}
  ${POSS_SHARE_PARAMETER_CHECK_ERROR_BUCKET}
  ${POSS_SHARE_PARAMETER_CHECK_ERROR_KEY_1}
  ${POSS_SHARE_PARAMETER_CHECK_ERROR_KEY_2}
  ${POSS_SHARE_PARAMETER_CHECK_ERROR_KEY_3}
  ${POSS_SHARE_PARAMETER_CHECK_ERROR_KEY_4}
  ${POSS_SHARE_PARAMETER_CHECK_SHARE_DIR}

Test poss renew parameter check
  [Template]   Test poss renew parameter check ${param}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_BUCKET}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_KEY}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_CHIPRICE_1}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_CHIPRICE_2}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_CHIPRICE_3}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_COPIES_1}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_COPIES_2}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_COPIES_3}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_EXPIRES_1}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_EXPIRES_2}
  ${POSS_RENEW_PARAMETER_CHECK_ERROR_EXPIRES_3}

Test poss copy parameter check
  [Template]   Test poss copy parameter check ${param}
  ${POSS_COPY_PARAMETER_CHECK_ERROR_KEY}
  ${POSS_COPY_PARAMETER_CHECK_ERROR_SOURCE}
  ${POSS_COPY_PARAMETER_CHECK_ERROR_CHIPRICE}
  ${POSS_COPY_PARAMETER_CHECK_ERROR_COPIES}
  ${POSS_COPY_PARAMETER_CHECK_ERROR_EXPIRES}

Test poss put get delete
  [Template]    Test poss put get delete ${param}
  ${POSS_PUT_GET_DELETE_1K}
  ${POSS_PUT_GET_DELETE_16LESSM}
  ${POSS_PUT_GET_DELETE_16LARGERM}
  ${POSS_PUT_GET_DELETE_32M_2COPIES}

Test poss put move get delete
  [Template]    Test poss put move get delete ${param}
  ${POSS_PUT_MOVE_GET_DELETE_1K}
  ${POSS_PUT_MOVE_GET_DELETE_1K_2COPIES}
  ${POSS_PUT_MOVE_GET_DELETE_1K_2COPIES_BETWEEN_BUCKETS}
  ${POSS_PUT_MOVE_GET_DELETE_32M_2COPIES_BETWEEN_BUCKETS}

Test poss put share get delete get
  [Template]    Test poss put share get delete get ${param}
  ${POSS_PUT_SHARE_GET_DELETE_GET_1K}
  ${POSS_PUT_SHARE_GET_DELETE_GET_32M_2COPIES}

Test poss put move share get delete
  [Template]    Test poss put move share get delete ${param}
  ${POSS_PUT_MOVE_SHARE_GET_DELETE_1K}
  ${POSS_PUT_MOVE_SHARE_GET_DELETE_32M_2COPIES}

Test poss put copy get delete
  [Template]    Test poss put copy get delete ${param}
  ${POSS_PUT_COPY_GET_DELETE_1K}
  ${POSS_PUT_COPY_GET_DELETE_32M}
  ${POSS_PUT_COPY_GET_DELETE_1K_2COPIES_BETWEEN_BUCKETS}
  ${POSS_PUT_COPY_GET_DELETE_32M_2COPIES_BETWEEN_BUCKETS}

Test poss put move copy get delete
  [Template]    Test poss put move copy get delete ${param}
  ${POSS_PUT_MOVE_COPY_GET_DELETE_1K}
  ${POSS_PUT_MOVE_COPY_GET_DELETE_32M}
  ${POSS_PUT_MOVE_COPY_GET_DELETE_1K_2COPIES}
  ${POSS_PUT_MOVE_COPY_GET_DELETE_32M_2COPIES}

Test poss put copy move get delete
  [Template]    Test poss put copy move get delete ${param}
  ${POSS_PUT_COPY_MOVE_GET_DELETE_1K}
  ${POSS_PUT_COPY_MOVE_GET_DELETE_32M}
  ${POSS_PUT_COPY_MOVE_GET_DELETE_1K_2COPIES}
  ${POSS_PUT_COPY_MOVE_GET_DELETE_32M_2COPIES}

Test poss put renew get delete
  [Template]    Test poss put renew get delete ${param}
  ${POSS_PUT_RENEW_GET_DELETE_1K_INCREATE_CHIPRICE_COPIES_EXPIRES}
  ${POSS_PUT_RENEW_GET_DELETE_32M_INCREATE_CHIPRICE_COPIES_EXPIRES}
  ${POSS_PUT_RENEW_GET_DELETE_1K_DECREASE_COPIES}
  ${POSS_PUT_RENEW_GET_DELETE_32M_DECREASE_COPIES}
  ${POSS_PUT_RENEW_GET_DELETE_1K_DECREASE_CHIPRICE}
  ${POSS_PUT_RENEW_GET_DELETE_32M_DECREASE_CHIPRICE}

Test poss put renew move get delete
  [Template]    Test poss put renew move get delete ${param}
  ${POSS_PUT_RENEW_MOVE_GET_DELETE_1K}
  ${POSS_PUT_RENEW_MOVE_GET_DELETE_32M}

Test poss put renew copy get delete
  [Template]    Test poss put renew copy get delete ${param}
  ${POSS_PUT_RENEW_COPY_GET_DELETE_1K}
  ${POSS_PUT_RENEW_COPY_GET_DELETE_32M}

Test put pause resume get delete ${param}
  [Template]    Test put pause resume get delete ${param}
  ${POSS_PUT_PAUSE_RESUME_GET_DELETE_64M_25}
  ${POSS_PUT_PAUSE_RESUME_GET_DELETE_64M_2COPIES_25}
  ${POSS_PUT_PAUSE_RESUME_GET_DELETE_64M_50}
  ${POSS_PUT_PAUSE_RESUME_GET_DELETE_64M_2COPIES_50}

Test put get pause resume delete
  [Template]    Test put get pause resume delete ${param}
  ${POSS_PUT_GET_PAUSE_RESUME_DELETE_64M_25}
  ${POSS_PUT_GET_PAUSE_RESUME_DELETE_128M_50}

Test put share get pause resume delete
  [Template]    Test put share get pause resume delete ${param}
  ${POSS_PUT_SHARE_GET_PAUSE_RESUME_DELETE_64M_25}
  ${POSS_PUT_SHARE_GET_PAUSE_RESUME_DELETE_128M_50}

Test put copy pause resume get delete
  [Template]    Test put copy pause resume get delete ${param}
  ${POSS_PUT_COPY_PAUSE_RESUME_GET_DELETE_64M_25}
  ${POSS_PUT_COPY_PAUSE_RESUME_GET_DELETE_128M_55}

*** Key Words ***
Test create bucket parameter check ${param}
  create bucket    ${param}

Test create same bucket ${param}
  create bucket    ${param}[first]
  create bucket    ${param}[second]

Test delete bucket parameter check ${param}
  delete bucket    ${param}

Test delete not empty bucket ${param}
  put object    ${param}[put]
  delete bucket    ${param}[delete]

Test create dir ${param}
  put object    ${param}
  delete object    ${param}

Test poss put parameter check ${param}
  put object    ${param}

Test poss get parameter check ${param}
  get object    ${param}

Test poss delete parameter check ${param}
  delete object    ${param}

Test poss share parameter check ${param}
  share object    ${param}

Test poss renew parameter check ${param}
  renew object    ${param}

Test poss copy parameter check ${param}
  copy object    ${param}

Test poss put get delete ${param}
  put object    ${param}[put]
  get object    ${param}[get]
  delete object    ${param}[delete]

Test poss put move get delete ${param}
  put object    ${param}[put]
  move object    ${param}[move]
  get object    ${param}[get]
  delete object    ${param}[delete]

Test poss put share get delete get ${param}
  put object    ${param}[put]
  ${share_code} =    share object    ${param}[put]
  get object    ${param}[get]    ${share_code}
  delete object    ${param}[delete]
  get object    ${param}[failget]    ${share_code}

Test poss put move share get delete ${param}
  put object    ${param}[put]
  move object    ${param}[move]
  ${share_code} =    share object    ${param}[move]
  get object    ${param}[get]    ${share_code}
  delete object    ${param}[delete]

Test poss put copy get delete ${param}
  put object    ${param}[put]
  copy object    ${param}[copy]
  get object    ${param}[get]
  delete object    ${param}[put]
  delete object    ${param}[copy]

Test poss put move copy get delete ${param}
  put object    ${param}[put]
  move object    ${param}[move]
  copy object    ${param}[copy]
  get object    ${param}[get]
  delete object    ${param}[move]
  delete object    ${param}[copy]

Test poss put copy move get delete ${param}
  put object    ${param}[put]
  copy object    ${param}[copy]
  move object    ${param}[move]
  get object    ${param}[get]
  delete object    ${param}[put]
  delete object    ${param}[move]

Test poss put renew get delete ${param}
  put object    ${param}[put]
  renew object    ${param}[renew]
  get object    ${param}[get]
  delete object    ${param}[put]

Test poss put renew move get delete ${param}
  put object    ${param}[put]
  renew object    ${param}[renew]
  move object    ${param}[move]
  get object    ${param}[get]
  delete object    ${param}[move]

Test poss put renew copy get delete ${param}
  put object    ${param}[put]
  renew object    ${param}[renew]
  copy object    ${param}[copy]
  get object    ${param}[get]
  delete object    ${param}[put]
  delete object    ${param}[copy]

Test put pause resume get delete ${param}
  ${task} =    put object    ${param}[put]
  pause task    ${param}[pause]    ${task}
  resume task    ${param}[put]    ${task}
  check object status    ${param}[put]
  get object    ${param}[get]
  delete object    ${param}[put]

Test put get pause resume delete ${param}
  put object    ${param}[put]
  ${task} =    get object    ${param}[get]
  pause task    ${param}[pause]    ${task}
  resume task    ${param}[get]    ${task}
  delete object    ${param}[put]

Test put share get pause resume delete ${param}
  put object    ${param}[put]
  ${share_code} =    share object    ${param}[put]
  ${task} =    get object    ${param}[get]    ${share_code}
  pause task    ${param}[pause]    ${task}
  resume task    ${param}[pause]    ${task}
  delete object    ${param}[put]

Test put copy pause resume get delete ${param}
  put object    ${param}[put]
  ${task} =    copy object    ${param}[copy]
  pause task    ${param}[pause]    ${task}
  resume task    ${param}[pause]    ${task}
  get object    ${param}[get]
  delete object    ${param}[put]
  delete object    ${param}[copy]
