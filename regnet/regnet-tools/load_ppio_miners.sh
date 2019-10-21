#!/bin/bash
# date:   2018-09-25
# author: Viktor <viktor@ppfs.io>
# usage:  load ppio's miner-id into redis

echo "------------------------------------------------"
BASE_DIR=$(dirname "$0")
PPIO_MINER_LIST_FILE="${BASE_DIR}/ppio_miner_list.ini"
echo "PPIO_MINER_LIST_FILE=${PPIO_MINER_LIST_FILE}"
CLI="redis-cli"
REDIS_CLI_PATH=`which ${CLI}`
if [ -z ${REDIS_CLI_PATH} ]; then
    echo "please install redis-cli!"
    exit 1
fi

REDIS_KEY="Miners.PPIO"

redis-cli DEL ${REDIS_KEY}

while read -r line
do
    if [[ ${line} == \#* ]]; then
        continue
    fi
    if [[ -z ${line} ]]; then
        continue
    fi
    miner_id=${line}
    redis-cli -h 10.96.200.202 SADD ${REDIS_KEY} ${miner_id}
done < ${PPIO_MINER_LIST_FILE}
