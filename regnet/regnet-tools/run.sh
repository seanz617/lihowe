#!/bin/bash
######################################
#author: hongwei Liu
#date: 2018-10.26
#desc: run application in docker and redirect stdout&stderr to log file
#parameters:
	#for all node
	#$1 application branch, such as master test dev...
	#$2 application name, such as gppio ppio miner indexer...
	#$3 gppio no. 
        #$4 for AB test: A: main;B: test 
######################################
	
if [[ $# < 2 ]];then
	echo "parameters error"
	exit 1
fi

export PATH=$PATH:/usr/lib/go/bin
export GOPATH=/home/workspace/go
export GOBIN=/home/workspace/go/bin
export PATH=$PATH:$GOPATH:$GOPATH/bin:$GOBIN

work_dir=/home/workspace
config_dir=/home/regnet-config
gppio_dir=go/src/github.com/PPIO/ppio-chain
#go_enfi_dir=go/src/github.com/PPIO/go_enfi
go_enfi_dir=go/src/github.com/PPIO/go-ppio

ip=`ifconfig | grep 'inet 10.244.*.*' | grep -v '10.244.0.0' | awk '{print $2}'`
echo "host ip = $ip"

if [ $2 == 'gppio' ];then
	cd $work_dir/$gppio_dir

	echo 'delete last db files'
	rm -rf data.db/ miner.*.db normal.db/

	echo 'start normal'
	./gppio -c ./conf/example/normal.conf &> $work_dir/regnet-logs/$1/gppio/normal/logs &

	echo 'start miner.1'
	./gppio -c ./conf/example/miner.1.conf &> $work_dir/regnet-logs/$1/gppio/miner.1/logs &

	echo 'start miner.2'
	./gppio -c ./conf/example/miner.2.conf &> $work_dir/regnet-logs/$1/gppio/miner.2/logs & 

	echo 'start miner.3'
	./gppio -c ./conf/example/miner.3.conf &> $work_dir/regnet-logs/$1/gppio/miner.3/logs &

	echo 'start default'
	./gppio -c ./conf/default/config.conf &> $work_dir/regnet-logs/$1/gppio/default/logs

	#cd $work_dir/$go_enfi_dir/cmd/paymentproxy
	#./paymentproxy &
	#cd $work_dir/$go_enfi_dir/cmd/gateway
	#./gateway --rpchost=0.0.0.0 --bindip=0.0.0.0 --daemon
fi

if [ $2 == 'bootstrap' ];then
	cd $work_dir/$go_enfi_dir
	
	cfg_file=$config_dir/$1/$2$3/$2.conf

	echo "starting $2$3 process"
	echo "testnet=$4"

	if [ ! -n "$4" ] ;then
		./cmd/$2/$2 daemon --rpchost=$ip --bindip=$ip --config=$cfg_file --daemon --datadir=%config_dir/$1/$2$3 &> $work_dir/regnet-logs/$1/$2$3/logs
	else
		./cmd/$2/$2 daemon --rpchost=$ip --bindip=$ip --config=$cfg_file --daemon --testnet=$4 --datadir=%config_dir/$1/$2$3 &> $work_dir/regnet-logs/$1/$2$3/logs
	fi		
fi

if [ $2 == 'center' ]; then
	cd $work_dir/$go_enfi_dir
	
	/etc/init.d/redis-server start

	cfg_file=$config_dir/$1/$2$3/$2.conf

	echo "reading $2$3 config"
	rpc_host=` awk '$1~/\[.*/{_cdr_par_=0}\
         	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*rpc_host *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	rpc_port=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*rpc_port *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	tcp_port=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*tcp_port *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	udp_port=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*udp_port *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`
	
	redis_host=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*redis_host *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	redis_port=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*redis_port *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	redis_db=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*redis_db *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	bind_ip=` awk '$1~/\[.*/{_cdr_par_=0}\
         	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*bind_ip *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	echo "rpc_host=$ip"
	echo "rpc_port=$rpc_port"
	echo "tcp_port=$tcp_port"
	echo "udp_port=$udp_port"
	echo "redis_host=$redis_host"
	echo "redis_port=$redis_port"
	echo "redis_db=$redis_db"
	echo "bind-ip=$ip"
	echo "testnet=$4"

	echo "starting $2$3 process"
	if [ ! -n "$4" ] ;then
		./cmd/$2/$2 --rpchost=$ip --rpcport=$rpc_port --tcpport=$tcp_port --udpport=$udp_port --redishost=$redis_host --redisport=$redis_port --redisdb=$redis_db --bindip=$ip --datadir=$config_dir/$1/$2$3 --daemon &> $work_dir/regnet-logs/$1/$2$3/logs
	else
		./cmd/$2/$2 --rpchost=$ip --rpcport=$rpc_port --tcpport=$tcp_port --udpport=$udp_port --redishost=$redis_host --redisport=$redis_port --redisdb=$redis_db --bindip=$ip --datadir=$config_dir/$1/$2$3 --daemon --testnet=$4 &> $work_dir/regnet-logs/$1/$2$3/logs
	fi
fi

if [ $2 == 'verifier' ]; then
	cd $work_dir/$go_enfi_dir

	cfg_file=$config_dir/$1/$2$3/$2.conf

	echo "starting $2$3 process"

	if [ ! -n "$4" ] ;then
		./cmd/$2/$2 --daemon --rpchost=$ip --bindip=$ip --config=$cfg_file --datadir=$config_dir/$1/$2$3 &> $work_dir/regnet-logs/$1/$2$3/logs </dev/null
	else
		./cmd/$2/$2 --daemon --rpchost=$ip --bindip=$ip --config=$cfg_file --datadir=$config_dir/$1/$2$3 --testnet=$4 &> $work_dir/regnet-logs/$1/$2$3/logs </dev/null
	fi
fi

if [ $2 == 'indexer' ]; then
	cd $work_dir/$go_enfi_dir

	/etc/init.d/redis-server start

	cfg_file=$config_dir/$1/$2$3/indexer.json

	if [ ! -n "$4" ] ;then
		./cmd/$2/$2 --bindip=$ip --rpchost=$ip --daemon --config=$cfg_file --datadir=$config_dir/$1/$2$3 &> $work_dir/regnet-logs/$1/$2$3/logs </dev/null
	else
		./cmd/$2/$2 --bindip=$ip --rpchost=$ip --daemon --config=$cfg_file --datadir=$config_dir/$1/$2$3 --testnet=$4 &> $work_dir/regnet-logs/$1/$2$3/logs </dev/null
	fi
fi

if [ $2 == 'paymentproxy' ]; then
	cd $work_dir/$go_enfi_dir

	/etc/init.d/redis-server start

	cfg_file=$config_dir/$1/$2$3/

	echo "./$2 --conf=$cfg_file &> $work_dir/regnet-logs/$1/$2$3/logs"
	if [ ! -n "$4" ] ;then
		./$2 --conf=$cfg_file &> $work_dir/regnet-logs/$1/$2$3/logs
	else
		./$2 --conf=$cfg_file --test=$4 &> $work_dir/regnet-logs/$1/$2$3/logs
	fi
fi

if [ $2 == 'gateway' ]; then
	cd $work_dir/$go_enfi_dir

	/etc/init.d/redis-server start

	cfg_file=$config_dir/$1/$2$3/$2.conf

	gppio_host=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*gppio_host *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	gppio_port=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*gppio_port *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	rpc_port=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*rpc_port *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	tcp_port=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*tcp_port *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	udp_port=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*udp_port *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`
	
	indexer_ip=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*indexer_ip *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	indexer_tcp_port=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*indexer_tcp_port *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	indexer_udp_port=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*indexer_udp_port *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	indexer_id=` awk '$1~/\[.*/{_cdr_par_=0}\
          	$0 ~ /^ *\[ *network *\]/ {_cdr_par_=1}\
         	$0~/^[\011 ]*indexer_id *=.*/ { if(_cdr_par_==1) { sub("="," "); print $2; exit 0} }\
         	' ${cfg_file}`

	if [ ! -n "$4" ] ;then
		./cmd/$2/$2 --rpchost=$ip --bindip=$ip --rpcport=$rpc_port --tcpport=$tcp_port --udpport=$udp_port --indexerip=$indexer_ip --indexertcpport=$indexer_tcp_port --indexerudpport=$indexer_udp_port --indexerid=$indexer_id --nasnodeaddress=$gppio_host:$gppio_port --daemon --datadir=$config_dir/$1/$2$3 &> $work_dir/regnet-logs/$1/$2$3/logs
	else
		./cmd/$2/$2 --rpchost=$ip --bindip=$ip --rpcport=$rpc_port --tcpport=$tcp_port --udpport=$udp_port --indexerip=$indexer_ip --indexertcpport=$indexer_tcp_port --indexerudpport=$indexer_udp_port --indexerid=$indexer_id --nasnodeaddress=$gppio_host:$gppio_port --daemon --testnet=$4 --datadir=$config_dir/$1/$2$3 &> $work_dir/regnet-logs/$1/$2$3/logs
	fi
fi

if [ $2 == 'user' ]; then
	cd $config_dir/$1/$2$3
	rm -rf *.db
	rm -rf storage/

	cd $work_dir/$go_enfi_dir
	echo "./poss --datadir=$config_dir/$1/$2$3 --config=$config_dir/$1/$2$3/poss.conf &> $work_dir/regnet-logs/$1/$2$3/logs"
	if [ ! -n "$4" ] ;then
		./cmd/poss/poss start-daemon --daemon --datadir=$config_dir/$1/$2$3 --config=$config_dir/$1/$2$3/poss.conf &> $work_dir/regnet-logs/$1/$2$3/logs </dev/null
	else
		./cmd/poss/poss start-daemon --daemon --datadir=$config_dir/$1/$2$3 --config=$config_dir/$1/$2$3/poss.conf --testnet=$4 &> $work_dir/regnet-logs/$1/$2$3/logs </dev/null
	fi
fi

if [ $2 == 'miner' ]; then
	cd $config_dir/$1/$2$3
	rm -rf *.db
	rm -rf miner-*/

	cd $work_dir/$go_enfi_dir
	if [ ! -n "$4" ] ;then
		./cmd/$2/$2 daemon --daemon --datadir=$config_dir/$1/$2$3 --config=$config_dir/$1/$2$3/miner.conf --storage-chiprice=100 --download-chiprice=100 &> $work_dir/regnet-logs/$1/$2$3/logs </dev/null
	else
		./cmd/$2/$2 daemon --daemon --datadir=$config_dir/$1/$2$3 --config=$config_dir/$1/$2$3/miner.conf --storage-chiprice=100 --download-chiprice=100 --testnet=$4 &> $work_dir/regnet-logs/$1/$2$3/logs </dev/null
	fi
fi

if [ $2 == 'jenkins' ]; then
	/etc/init.d/ssh start	
	top -b
fi

top -b
