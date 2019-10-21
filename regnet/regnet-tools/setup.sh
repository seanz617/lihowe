#!/bin/bash
#######################################################
#author: Hongwei Liu
#date: 2018-11-1
#desc: setup ppio&gppio docker cloud env base on kubernetes yaml config
#param: 
	#$1 kubernetes yaml config file dircetory. such as /home/nfs/kube-config
	#$2 forA/B test. such as A or B
#example: ./setup.sh /home/nfs/kube-config A
#######################################################

config_dir=$1
app_name=$2
app_branch=$3
app_no=0
if [[ $app_branch == 'B' ]];then
	app_no=1
fi

ppio_project_dir=/home/nfs/go/src/github.com/PPIO/go-ppio

function move_app() {
	currnet_dir=`pwd`

	cd $ppio_project_dir
	cp cmd/center/center         ./
        cp cmd/bootstrap/bootstrap   ./
        cp cmd/indexer/indexer       ./
        cp cmd/indexer/indexer.json  ./
        cp cmd/verifier/verifier     ./
        cp cmd/gateway/gateway       ./
        cp cmd/ppio/ppio             ./
        cp cmd/poss/poss             ./
        cp cmd/miner/miner           ./

	cd current_dir
}

function wait() {
	local len=0
	for i in {1..60}
	do
		len=`kubectl get pods | grep "$1" | grep "Running" | wc -c`
		if [[ $len > 4 ]]; then
			break
		fi
		sleep 5s
	done

	if [[ $len < 4 ]]; then
		echo "create $1 timeout"
		exit 1
	else
		echo "create $1 success"
	fi
}

function check() {
	local ret
	sleep 60s
	ret=`kubectl get pods | grep -v 'STATUS' | awk '{print $3}' | sed 's/ //g'`
	for pod in {$ret}
	do
		if [[ $pod != 'Running' && $pod != '{STATUS' ]]; then
			echo "some pod run exception"
			exit 1
		fi
	done
}

function deposit() {
	tools_dir=/home/workspace/regnet-tools
	echo 'deposit ...'
	gppio_pod=`kubectl get pods -o name | grep 'gppio'`
	echo ${gppio_pod#*/}
	kubectl exec ${gppio_pod#*/} -- $tools_dir/deposit.sh
}

function clear_db() {
	tools_dir=/home/workspace/regnet-tools
	echo 'deposit ...'
	mysql_pod=`kubectl get pods -o name | grep 'mysql'`
	echo ${mysql_pod#*/}
	kubectl exec ${mysql_pod#*/} -- $tools_dir/clear_db.sh
}

function load_ppio_miner() {
	tools_dir=/home/workspace/regnet-tools
	echo 'load ppio miners ...'
	indexer_pod=`kubectl get pods -o name | grep 'indexer'`
	echo ${indexer_pod#*/}
	kubectl exec ${indexer_pod#*/} -- $tools_dir/load_ppio_miner.sh
}

function clean() {

	kubectl delete rc --all
	kubectl delete pods --all
	for i in {1..60}
	do
		sleep 10s
		output=`kubectl get pods` 
		echo $output
		if [[ $output == '' ]]; then
			break
		fi
	done
	if [[ $output != '' ]]; then
		echo 'stop pod fail'
		exit 1
	else
		echo 'stop all pod success'
	fi
}

function setup_base() {
	kubectl create -f $config_dir/global/redis-rc.yml
	wait "redis" 
	kubectl create -f $config_dir/global/mysql-rc.yml
	wait "mysql" 
}

function setup_ELK() {
	kubectl create -f $config_dir/global/elasticsearch-rc.yml
	wait "elastic" 

	kubectl create -f $config_dir/global/logstash-rc.yml
	wait "logstash" 

	kubectl create -f $config_dir/global/kibana-rc.yml
	wait "kibana" 
}

function setup_gppio() {
	kubectl create -f $config_dir/global/gppio-new-rc.yml
	wait "gppio" 
}

function setup_ppio() {
	cp $ppio_project_dir/service/indexer/assets/ppio.sql /home/nfs/regnet-tools/

	if [[ $app_branch == 'A' ]];then
		./deploy.sh
		redis-cli -h 10.96.200.202 flushall
		mysql -h 10.96.200.217 -uroot -p123456 -Dppio < /home/nfs/regnet-tools/ppio.sql
	fi
	
	if [[ $app_branch == 'B' ]];then
		mysql -h 10.96.200.217 -uroot -p123456 -Dppiob < /home/nfs/regnet-tools/ppio.sql
	fi
	
	kubectl create -f $config_dir/env-$app_branch/pod/center$app_no-rc.yml
	wait "center" 

	kubectl create -f $config_dir/env-$app_branch/pod/bootstrap$app_no-rc.yml
	wait "bootstrap" 

	kubectl create -f $config_dir/env-$app_branch/pod/verifier$app_no-rc.yml
	wait "verifier" 

	kubectl create -f $config_dir/env-$app_branch/pod/indexer$app_no-rc.yml
	wait "indexer" 

	#kubectl create -f $config_dir/env-$app_branch/pod/payment$app_no-rc.yml
	#wait "payment"

	kubectl create -f $config_dir/env-$app_branch/pod/gateway$app_no-rc.yml
	wait "gateway" 

	if [[ $app_branch == 'A' ]];then
		deposit
	fi
}

if [[ $app_name == 'base' ]]; then
	setup_base
fi

if [[ $app_name == 'elk' ]]; then
	setup_ELK
fi

if [[ $app_name == 'gppio' ]]; then
	setup_gppio 
fi

if [[ $app_name == 'ppio' ]]; then
	setup_ppio
fi

if [[ $app_name == 'deposit' ]]; then
	deposit
fi

if [[ $app_name == 'move' ]]; then
	move_app	
fi
