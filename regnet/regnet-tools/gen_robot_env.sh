#!/bin/bash
#######################################
#author: Hongwei Liu
#date: 2018-11-22
#desc: install python pip and robot framework environment for test
#os: ubuntu 16.04
#python: 3.6.7
#pip: 9.0.1
#robot framework: 3.0.4
#######################################

if [ ! -n $1 ]; then
	echo "pls give [test-framework dir] parameter for python"
	exit 1
fi

pythonpath=$1

#install python 3 
apt-get install software-properties-common
add-apt-repository ppa:jonathonf/python-3.6
apt-get update
apt-get install python3.6

#install pip
apt-get install python3-pip

#link python3 -> python and pip3 -> pip
cd /usr/bin
ln -s python3.6m python
ln -s pip3 pip

#check python and pip install
python -V
pip -V

#install robot framework
pip install robotframework
pip install robotframework-archivelibrary
pip install robotframework-sshlibrary
pip install robotframework-requests

#check robot install
robot --version

#install kubernetes for python
pip install kubernetes

#prepare pythonpath 
export PYTHONPATH=$PYTHONPATH:$pythonpath
