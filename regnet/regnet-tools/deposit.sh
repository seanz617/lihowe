#!/bin/bash
####################################
#author: Hongwei Liu
#date: 2018-11-15
#desc: run gppio deposit without modify source code
####################################

cd /home/workspace/go/src/github.com/PPIO/ppio-chain
chmod 0755 ./transfer_center2accounts.sh
chmod 0755 ./transfer_accounts2holder.sh
./transfer_center2accounts.sh
./transfer_accounts2holder.sh
cd ~
