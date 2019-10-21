*** Settings   ***
Library    controller.test_env
Library    controller.test_miner
Library    controller.test_indexer
Library    controller.test_poss
Variables    data-center/data.py

*** Test Cases ***
Test indexer reschedual
  [Template]    Test indexer reschedual ${param}
  ${INDEXER_RESCHEDUAL}

*** Key Words ***
Test indexer reschedual ${param}
  clear storage contracts    ${param}[indexer]
  put object    ${param}[put1]
  put object    ${param}[put2]
  renew object    ${param}[renew]
  stop miner    ${param}[stop1] 
  BuiltIn.Sleep   180s
  check object status    ${param}[check1]
  put object    ${param}[put3]
  BuiltIn.Sleep   120s
  check object status    ${param}[check2]
  stop miner    ${param}[stop2]
  BuiltIn.Sleep   180s
  check object status    ${param}[check3]
