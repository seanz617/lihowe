#~/bin/bash
####################################
#author: Hongwei Liu
#date: 2018-12-3
#desc: sync time between vm 
####################################

function sync() {
	scp /home/nfs/regnet-tools/adjust_time.sh root@192.168.50.$1:./
	ssh root@192.168.50.$1 chmod 0777 ./adjust_time.sh

	ssh root@192.168.50.$1 ./adjust_time.sh 
}

for((i=231;i<235;i++))
do
	deploy $i
done

for((i=239;i<243;i++))
do
	deploy $i
done
