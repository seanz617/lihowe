#!/bin/bash
#author: Hongwei Liu
#date: 2018-11-27
#desc: run test cases and delete reports a month ago
#example: ./run_test.sh

source ~/.bashrc

branch_name=$1
report_title=$2

base_dir=$(cd `dirname $0`; pwd)
case_dir=${base_dir}/cases/submit
report_dir=/home/workspace/report

#prepare python environment
export PYTHONPATH=/home/workspace
export PYTHONPATH=$PYTHONPATH:${base_dir}
export PYTHONPATH=$PYTHONPATH:${base_dir}/utils
export PYTHONPATH=$PYTHONPATH:${base_dir}/controller
export PYTHONPATH=$PYTHONPATH:${base_dir}/config
export PYTHONPATH=$PYTHONPATH:${base_dir}/model
export TEST_CONFIG=${base_dir}/config/test_config.json
export TEST_ENV=S
export TEST_SUBENV=A

#get commit id
cd ${GOPATH}/src/github.com/PPIO/go-ppio
commit_id=`git log --pretty=format:"%h - %an, %ar : %s" -n 1 | awk '{print $1}'`

#run test cases
cd $base_dir
robot --name="$report_title" $case_dir/test_env.robot $case_dir/test_ppio.robot $case_dir/test_env.robot
test_result=`cat output.xml | grep 'All Tests' | awk -F'[ >="]' '{print $4,$8,$4+$8}'`
python add_commit_id.py ${branch_name} ${commit_id}

#clear last report
rm -rf $report_dir
mkdir $report_dir
cp log.html ${report_dir}/
cp report.html ${report_dir}/
cp output.xml ${report_dir}/

python discord_bot.py ${branch_name} ${commit_id} "${report_title}" "${test_result}"
