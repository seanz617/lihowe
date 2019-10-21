#!/bin/bash
#######################################################
#author: Hongwei Liu
#date: 2018-11-10
#desc: add miner 
#param: 
	#$1 user or miner
	#$2 how many miners or users do you want to setup
#example: ./ppio_ops user 4
#######################################################

function wait() {
	local len=0
	for i in {1..30}
	do
		len=`kubectl get pods | grep "$1" | grep "Running" | wc -c`
		if [[ $len > 4 ]]; then
			break
		fi
		sleep 10s
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
	for i in {1..7}
	do
		ret=`kubectl get pods | awk '{print $3}' | sed 's/ //g'`
		for pod in {$ret}
		do
			if [[ $pod != 'Running' && $pod != '{STATUS' ]]; then
				echo "some pod run exception"
				exit 1
			fi
		done
	done
}

function clean() {
	kubectl delete rc --all
	kubectl delete pods --all
	for i in {1..60}
	do
		sleep 5s
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

count=0
flags=(0 0 0 0 0 0 0 0 0 0 0)
config_dir=/home/nfs/kube-config/global

for i in `kubectl get pods -o name | grep $1 | sed 's/[\/a-zA-Z]//g'`;
do
	flags[$i]=1
done

for ((i=0;i<10;i++))
do
	if [[ ${flags[$i]} -eq 1 ]]; then
		let count++
		if [[ $count -gt $2 ]]; then
			echo "kubectl delete pods $1$i"
			kubectl delete pods $1$i
			let count--
		fi
	elif [[ ${flagss[$i]} -eq 0 ]]; then
		if [[ $count -lt $2 ]]; then
			echo "kubectl create -f $config_dir/$1$i.yml"
			kubectl create -f $config_dir/$1$i.yml
			let count++
		fi
	fi
done
