*** Settings   ***
Library    utils.common
Library    controller.test_env
Library    controller.test_indexer
Variables    data-center/data.py 

*** Test Cases ***
Test clear storage contracts 
  [Template]    Test clear storage contracts ${param}
  ${CLEAR_STORAGE_CONTRACTS}

Test check test environment 
  [Template]    Test check test environment ${param}
  ${CHECK_ENV}

*** Key Words ***
Test clear storage contracts ${param}
  clear storage contracts    ${param}

Test check test environment ${param}
  check env    ${param}
