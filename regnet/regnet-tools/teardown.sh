#!/bin/bash
####################################################
#author Hongwei Liu
#deat 2018-11-1
#desc delete pods&replica-controler in kubernetes
#param:
	#$1 node type user or miner or ppio or gppio or global or all 
	#	user: delete all user
	#	miner: delete all miner
	#	ppio: delete center bootstrap verifier indexer payment gateway user miner
	#	gppio: delete all ppio and gppio
	#	global: delete ppio and gppio and redis and elasticsearch and kibana and logstash
	#$2 for A/B test. such as A or B
#example: ./clean gppio A
####################################################

app_branch=$2
app_no=0
if [[ $app_branch == 'B' ]];then
        app_no=1
fi

function clean() {

	#kubectl delete rc --all
	#kubectl delete pods --all
	for i in {1..60}
	do
		sleep 10s
		output=`kubectl get pods` 
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

function deluser() {
	for i in `kubectl get pods -o name | grep user`;
	do
		echo delete ${i#*/}
		kubectl delete pods ${i#*/}
	done
}

function delminer() {
	for i in `kubectl get pods -o name | grep miner`;
	do
		echo delete ${i#*/}
		kubectl delete pods ${i#*/}
	done
}

function delppio() {
	kubectl delete rc center$app_no
	kubectl delete rc bootstrap$app_no 
	kubectl delete rc indexer$app_no 
	kubectl delete rc verifier$app_no
	#kubectl delete rc paymentproxy$app_no
	kubectl delete rc gateway$app_no 
}

if [ $1 == 'user' ]; then
	deluser
fi

if [ $1 == 'miner' ]; then
	delminer
fi

if [ $1 == 'ppio' ]; then
	deluser
	delminer
	delppio
fi

if [ $1 == 'gppio' ]; then
	deluser
	delminer
	delppio
	kubectl delete rc gppio
fi

if [ $1 == 'global' ]; then
	clean
fi

