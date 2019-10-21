#!/usr/bin/env bash

if [ $# -ne 3 ]
then
    echo "Please input project_name commit_id report_path"
    echo "Examples: "
    echo "./collect_log.sh <project_name name> <commit_id> <report_path>"
    echo "./collect_log.sh submit 8ceba84 /home/workspace/go/src/github.com/PPIO/ppio-tests/cases/automation/robot-tests/result/history/20190717_120819_8ceba84"
    exit -1
fi

project_name=$1
commit_id=$2
report_path=$3

date=$(date +"%Y-%m-%d_%H-%M-%S")
contain=$(echo ${project_name} | grep "regnet")
if [ -z "${contain}" ]
then
    ppio_log_path="/home/workspace/ppio_log"
else
    ppio_log_path="/home/workspace/regnet-config/pcdn/"
fi
nfs_path="/home/nfs/PPIO_Log/pcdn_auto_test_log"
current_path=$(cd `dirname $0`; pwd)
tmp_log_path="${current_path}/../result/tmp_log"

if [ -d ${tmp_log_path} ]
then
    rm -rf ${tmp_log_path}/*
else
    mkdir -p ${tmp_log_path}
fi

for item in `ls ${ppio_log_path}`
do
    path="${ppio_log_path}/${item}"
    if [ -d ${path} ]
    then
        echo "Current path:" ${path}
        cd ${path}
        ls
        # process_name=${item}
        process_log_path="${tmp_log_path}/${item}"
        mkdir -p ${process_log_path}
        console_log_path="${process_log_path}/console"
        mkdir -p ${console_log_path}
        files=$(ls *.log 2> /dev/null | wc -l)
        if [ "${files}"x != "0"x ]
        then
            cp `ls *.log 2> /dev/null | grep -v std` ${process_log_path} 2> /dev/null
            cp `ls *.log 2> /dev/null | grep std` ${console_log_path} 2> /dev/null
            cp `ls *.log.* 2> /dev/null` ${console_log_path} 2> /dev/null
            rm -rf *.log *.log.*
        fi
        cd -
    fi
done

auto_report_path="${tmp_log_path}/auto_test_report"
mkdir -p ${auto_report_path}
cp ${report_path}/* ${auto_report_path}
cd ${tmp_log_path}
tar_name="${project_name}_${date}_${commit_id}.tar.gz"
tar -zcvf ${tar_name} ./*
tar_file="${tmp_log_path}/${tar_name}"
cd -

if [ -z "${contain}" ]
then
    sshpass -p pplive123 scp ${tar_file} ppuser@192.168.50.206:"${nfs_path}/${project_name}"
else
    cp ${tar_file} "${nfs_path}/${project_name}"
fi
# rm -rf ${tar_file}
