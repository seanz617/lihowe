#author: Hongwei Liu
#date: 2018-12-27 
#desc: concurrent test from poss 
#example: python concurrent_test.py rate
#rate: put:get operations probability with float type and less than 1

import os,sys
import subprocess
import multiprocessing
import time
import datetime
import random
import commands

users = [
	("192.168.50.241",18060),
	#("192.168.50.241",18061),	
	#("192.168.50.240",18064),	
	#("192.168.50.240",18065),	
	#("192.168.50.239",18067),
	#("192.168.50.239",18068),
	#("192.168.50.239",18069)	
	]

put_body = [
	"/home/workspace/test-framework/data/16M",
	"/home/workspace/test-framework/data/32M",
	"/home/workspace/test-framework/data/64M",
	]

get_body = [
	"16M",
	"32M",
	"64M",
	]

def trace(pmethod, ptag, pmsg):
	with open('./trace_log', 'a') as tracefile:
		tracefile.write(pmethod + ":" + ptag + ":" + pmsg + "\n")

def put(num, ind):
	count = 1
	user_index = num
	user_addr = users[user_index][0]
	user_port = users[user_index][1]

	with open('./put_log' + str(num), 'a') as logfile:
		for body in put_body:
			run_cmd = "./poss {} --rpchost={} --rpcport={} --bucket={} --key={} --body={} --chiprice={} --expires={} --copies={}".format("put-object",user_addr,user_port,"tttt","/objj"+str(num*100+ind)+str(count),body,"100","2019-01-02","1")
			count = count + 1
			print(run_cmd + "\n")

			time.sleep(random.randint(1,10))

			start_time = int(time.time())
			proc = subprocess.Popen(run_cmd,shell=True,stdout=logfile,stderr=logfile)
			proc.wait()
			end_time = int(time.time())

			msg = "{}:{}:{}".format(str(start_time),str(end_time),str(end_time-start_time))
			trace("put", body, msg)

def get(num, ind):
	user_index = num
	user_addr = users[user_index][0]
	user_port = users[user_index][1]

	with open('./get_log' + str(num), 'a') as logfile:
		for body in get_body:
			run_cmd = "./poss {} --rpchost={} --rpcport={} --bucket={} --key={} --outfile={} --chiprice={}".format("get-object",user_addr,user_port,"tttt","/user"+str(user_port)+"file"+body,"./"+str(user_port),"100")
			print(run_cmd + "\n")

			time.sleep(random.randint(1,10))

			start_time = int(time.time())
			proc = subprocess.Popen(run_cmd,shell=True,stdout=logfile,stderr=logfile)
			proc.wait()
			end_time = int(time.time())

			msg = "{}:{}:{}".format(str(start_time),str(end_time),str(end_time-start_time))
			trace("get", body, msg)

parallel_num = int(sys.argv[2])
pool = []
pool.append(multiprocessing.Pool(processes = parallel_nm))
#pool.append(multiprocessing.Pool(processes = parallel_nm))
#pool.append(multiprocessing.Pool(processes = parallel_nm))
#pool.append(multiprocessing.Pool(processes = parallel_nm))
#pool.append(multiprocessing.Pool(processes = parallel_nm))
#pool.append(multiprocessing.Pool(processes = parallel_nm))
#pool.append(multiprocessing.Pool(processes = parallel_nm))
#pool.append(multiprocessing.Pool(processes = parallel_nm))
#pool.append(multiprocessing.Pool(processes = parallel_nm))
#pool.append(multiprocessing.Pool(processes = parallel_nm))

rate = float(sys.argv[1])
barrier = int(100 * rate)

def run(proc_no):
	for i in xrange(2):
		selector = random.randint(1,100)
		try:
			if selector <= barrier:
        			pool[proc_no].apply_async(put, (proc_no, i, )) 
			elif selector > barrier:
				pool[proc_no].apply_async(get, (proc_no, i, ))
		except Exception as e:
			print(e)

for i in range(6):
    run(i)

for item in pool: 
	item.close()
	item.join()
