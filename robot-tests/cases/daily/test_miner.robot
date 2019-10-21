*** Settings   ***
Library    controller.test_env
Library    controller.test_miner
Library    controller.test_indexer
Library    controller.test_poss
Variables    data-center/data.py

*** Test Cases ***
Test miner will leave ${param}
  [Template]    Test miner will leave ${param}
  ${MINER_WILL_LEAVE}

Test miner clear chunks
  [Template]    Test miner clear chunks ${param}
  ${MINER_CLEAR_CHUNKS_0}
  ${MINER_CLEAR_CHUNKS_1}

*** Key Words ***
Test miner will leave ${param}
  miner will leave    ${param}[willleave]
  put object    ${param}[put]

Test miner clear chunks ${param}
  clear storage contracts    ${param}[indexer]
  clear miner    ${param}[miner]
