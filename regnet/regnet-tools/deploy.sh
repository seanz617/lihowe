#~/bin/bash
####################################
#author: Hongwei Liu
#date: 2018-11-11
#desc: push config to every virtual machine 
####################################

function deploy() {
	ssh root@192.168.50.$1 rm -rf /home/regnet-config 
	ssh root@192.168.50.$1 rm -rf /root/regnet-config.tar.gz 
	scp /home/nfs/regnet-config.tar.gz root@192.168.50.$1:/home/
	ssh root@192.168.50.$1 tar -zxvf /home/regnet-config.tar.gz
	ssh root@192.168.50.$1 cp -r /root/regnet-config /home/
	ssh root@192.168.50.$1 rm -rf /root/regnet-config
	ssh root@192.168.50.$1 rm -rf /root/*.sh
	ssh root@192.168.50.$1 rm -rf /root/regnet-config.tar.gz
	ssh root@192.168.50.$1 chmod -R 0777 /home/regnet-config
}

deploy 208 

for((i=231;i<235;i++))
do
	deploy $i
done

for((i=239;i<243;i++))
do
	deploy $i
done
