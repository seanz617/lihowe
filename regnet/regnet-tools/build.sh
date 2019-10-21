#!/bin/bash
##########################################
#author: hongwei Liu
#date: 2018-10.30
#desc: build go project 
##########################################

export PATH=$PATH:/usr/lib/go/bin
export GOPATH=/home/workspace/go
export GOBIN=/home/workspace/go/bin
export PATH=$PATH:$GOPATH:$GOPATH/bin:$GOBIN

work_dir=/home/workspace
gppio_dir=go/src/github.com/PPIO/ppio-chain
go_enfi_dir=go/src/github.com/PPIO/go_enfi

cd $work_dir/$go_enfi_dir
make

cd $work_dir/$gppio_dir
make dep
make deploy-v8
make build
