#~/bin/bash
#if [[ $# != 2 ]];then
#	echo 'pls give the hostname parameter'
#	exit 1
#fi

#set hostname and hosts
#scp root@192.168.50.206:/etc/hosts /etc/hosts
#hostnamectl set-hostname $1

#prepare environment for kubernetes
#scp root@192.168.50.206:~/env-tools/prepare_env.sh ./
./prepare_env.sh 

#install docker version 17.03.2 wether other version is ok? try it 
#scp root@192.168.50.206:~/docker-ce-* ./
#yum localinstall -y docker-ce-17.03.2.ce-1.el7.centos.x86_64.rpm docker-ce-selinux-17.03.2.ce-1.el7.centos.noarch.rpm 
#scp root@192.168.50.206:/etc/docker/daemon.json /etc/docker/
#verify docker install
systemctl enable docker
systemctl start docker.service
docker version
if [ $? != 0 ]; then
	echo 'docker install failed'
	exit 1	
fi
#rm -rf docker-ce-*

#copy repos config
#scp root@192.168.50.206:/etc/yum.repos.d/docker.repo /etc/yum.repos.d/
#scp root@192.168.50.206:/etc/yum.repos.d/kubernetes.repo /etc/yum.repos.d/
#scp root@192.168.50.206:/etc/sysctl.d/k8s.conf /etc/sysctl.d/
modprobe br_netfilter
#sysctl -p /etc/sysctl.d/k8s.conf

#install kubeadm kubelet kubectl kubernetes-cni
echo "KUBELET_EXTRA_ARGS=--fail-swap-on=false" > /etc/sysconfig/kubelet 
yum makecache fast
#yum install -y kubelet kubeadm kubectl kubernetes-cni

#verify kubeadm install
swapoff  -a
sysctl -p /etc/sysctl.d/k8s.conf 
kubeadm version
systemctl enable kubelet.service

#notify master that a new node join in the cluster
#scp root@192.168.50.206:/etc/kubernetes/admin.conf /etc/kubernetes/admin.conf
#echo 'export KUBECONFIG=/etc/kubernetes/admin.conf' >> ~/.bashrc 
#source ~/.bashrc
#kubeadm join 192.168.50.206:6443 --token $2 --discovery-token-unsafe-skip-ca-verification
echo '--------Completed-------'
