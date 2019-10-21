#!/usr/bin/env bash

if [ $# -ne 1 ]
then
    echo "Please input regnet pods action"
    echo "Examples: "
    echo "./regnet_pods_controller.sh <action>"
    echo "./run_pcdn_single.sh restart"
    echo "./run_pcdn_single.sh stop"
    exit -1
fi

action=$1
service_pods_type=(coinpool mapping tracker)
ppio_pods_type=(peer)
#env_pods_type=(mysql redis)
env_pods_type=()


echo "Regnet all pods:"
kubectl get pods
echo "Regnet all rc:"
kubectl get rc


function stop_rc(){
    stop_pods_type=(${ppio_pods_type[@]} ${service_pods_type[@]} ${env_pods_type[@]})
    for type in ${stop_pods_type[@]}
    do
        all_rc=(${all_rc[@]} `kubectl get rc | grep ${type} | awk '{print $1}'`)
    done

    for e in ${all_rc[@]}
    do
        kubectl delete rc ${e}
    done
}

function start_pods(){
    yaml_path="/home/kube-config/pcdn/"
    cd ${yaml_path}
    create_pods_type=(${env_pods_type[@]} ${service_pods_type[@]} ${ppio_pods_type[@]})
    for pod in ${create_pods_type[@]}
    do
        files=`ls ${yaml_path} | grep ${pod} 2> /dev/null`
        for f in ${files[@]}
        do
            path="${yaml_path}/${f}"
            kubectl create -f ${path}
        done
#        if [ ${#files[@]} -ne 0 ]
#        then
#            kubectl create -f `ls ${yaml_path} | grep pod 2> /dev/null`
#        fi
    done
    cd -
}

function check_pod_status(){
    echo "Check pod $1 status"
    name=`kubectl get pods | grep $1 | awk '{print $1}'`
    status=`kubectl get pods | grep $1 | awk '{print $3}'`
    if [ -z "${name}" -o -z "${status}" ]
    then
        return 0
    fi

    echo "pod: ${name}; status: ${status}; expectation: $2"
    if [ "${status}"x == "${2}"x ]
    then
        return 0
    else
        return 1
    fi
}

function wait_pods_status(){
    expectation_status=$1
    start_pods_type=(${env_pods_type[@]} ${service_pods_type[@]} ${ppio_pods_type[@]})
    for type in ${start_pods_type[@]}
    do
        all_pods=(${all_pods[@]} `kubectl get pods | grep ${type} | awk '{print $1}'`)
    done
    for pod in ${all_pods[@]}
    do
        for i in $(seq 5)
        do
            check_pod_status ${pod} ${expectation_status}
            if [ "$?"x == "0"x ]
            then
                break
            else
                sleep 10
            fi
        done

        check_pod_status ${pod} ${expectation_status}
        if [ "$?"x != "0"x ]
        then
            echo "${pod} status error"
            exit 1
        fi
    done
}


if [ "${action}"x == "stop"x ]
then
    stop_rc
    wait_pods_status "Terminating"
fi

if [ "${action}"x == "restart"x ]
then
    stop_rc
    wait_pods_status "Terminating"

    start_pods
    wait_pods_status "Running"
fi


echo "Regnet all pods:"
kubectl get pods
echo "Regnet all rc:"
kubectl get rc
