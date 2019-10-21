#!/bin/bash
#######################################################
#authro: Hongwei Liu
#date: 2018-11-1
#desc: check all pods of kubernetes is running or not
#######################################################

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

check
