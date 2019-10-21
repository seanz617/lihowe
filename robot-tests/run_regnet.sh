#!/bin/bash
#author: Hongwei Liu
#date: 2018-11-27
#desc: run test cases and delete reports a month ago 
#example: ./run_test.sh

source ~/.bashrc
case_dir=/home/workspace/robot-tests/cases/daily

#prepare python environment
export PYTHONPATH=/home/workspace
export PYTHONPATH=$PYTHONPATH:/home/workspace/robot-tests
export PYTHONPATH=$PYTHONPATH:/home/workspace/robot-tests/utils
export PYTHONPATH=$PYTHONPATH:/home/workspace/robot-tests/controller
export PYTHONPATH=$PYTHONPATH:/home/workspace/robot-tests/config
export PYTHONPATH=$PYTHONPATH:/home/workspace/robot-tests/model
export TEST_CONFIG=/home/workspace/robot-tests/config/test_config.json
export TEST_ENV=R
export TEST_SUBENV=A

#run test cases
#dirdate=`date +%Y%m%d`_`date +%H%M%S`
#mkdir $dirdate
#cd $dirdate
robot $case_dir/env.robot $case_dir/ppio.robot $case_dir/buckets.robot $case_dir/poss.robot $case_dir/tasks.robot $case_dir/parameters.robot $case_dir/env.robot

#add commit id to report
mv report.html tmp.html
python ./add_commit_id.py ./property.txt ./tmp.html $1 > ./report.html
rm -rf ./tmp.html

#generate image
./phantomjs ./gen_image.js ./report.html ./report.png

#send image to slack
#cat output.xml | grep 'All Tests' | awk -F'[ >=]' '{print $3}'
#cat output.xml | grep 'All Tests' | awk -F'[ >=]' '{print $5}'
test_result=`cat output.xml | grep 'All Tests' | awk -F'[ >="]' '{print $4,$8,$4+$8}'`
python ./discord_bot.py "$test_result"

#move report
#rm -rf ../log.html
#rm -rf ../report.html
#rm -rf ../output.xml
#rm -rf ../report.png
#cp log.html ../ 
#cp report.html ../ 
#cp output.xml ../
#cp report.png ../

#cd ..
#sync log
ssh root@192.168.50.206 python /home/nfs/regnet-tools/sync_log.py /home/nfs/daily_auto_test_for_$1/$dirdate/log.tar.gz

#delete report a month ago
#mv $dirdate ./history/

#history_dir='./history/'
#today=$(date +%Y%m%d)
#last_month=`date -d last-month +%Y%m%d`
#tt1=`date -d $last_month +%s`

#for file in ${history_dir}*
#do
#	if test -d $file
#	then
#		full_name=`basename $file`
#		name=${full_name%_*}
#		curr=`date -d $name +%s`
#		if [[ $curr -le $tt1 ]]
#		then
#			rm -rf ${history_dir}${full_name}
#		fi
#	fi
#done

