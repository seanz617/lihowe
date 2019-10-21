#!/bin/bash
#########################################
#authori: Hongwei Liu
#date: 2018-11-1
#desc: pull images for kubernetes while you can't get these images from google website
#########################################

docker pull mirrorgooglecontainers/kube-apiserver:v1.12.1
docker pull mirrorgooglecontainers/kube-controller-manager:v1.12.1
docker pull mirrorgooglecontainers/kube-scheduler:v1.12.1
docker pull mirrorgooglecontainers/kube-proxy:v1.12.1
docker pull mirrorgooglecontainers/pause:3.1
docker pull mirrorgooglecontainers/etcd:3.2.24
docker pull coredns/coredns:1.2.2

docker tag mirrorgooglecontainers/kube-proxy:v1.12.1  k8s.gcr.io/kube-proxy:v1.12.1
docker tag mirrorgooglecontainers/kube-scheduler:v1.12.1 k8s.gcr.io/kube-scheduler:v1.12.1
docker tag mirrorgooglecontainers/kube-apiserver:v1.12.1 k8s.gcr.io/kube-apiserver:v1.12.1
docker tag mirrorgooglecontainers/kube-controller-manager:v1.12.1 k8s.gcr.io/kube-controller-manager:v1.12.1
docker tag mirrorgooglecontainers/etcd:3.2.24  k8s.gcr.io/etcd:3.2.24
docker tag coredns/coredns:1.2.2 k8s.gcr.io/coredns:1.2.2
docker tag mirrorgooglecontainers/pause:3.1  k8s.gcr.io/pause:3.1
 
docker rmi mirrorgooglecontainers/kube-apiserver:v1.12.1
docker rmi mirrorgooglecontainers/kube-controller-manager:v1.12.1
docker rmi mirrorgooglecontainers/kube-scheduler:v1.12.1
docker rmi mirrorgooglecontainers/kube-proxy:v1.12.1
docker rmi mirrorgooglecontainers/pause:3.1
docker rmi mirrorgooglecontainers/etcd:3.2.24
docker rmi coredns/coredns:1.2.2
