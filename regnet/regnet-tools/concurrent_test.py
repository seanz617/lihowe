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

put_body = [
	"/home/workspace/test-framework/data/32M.mp4",
	"/home/workspace/test-framework/data/256M.mp4",
	"/home/workspace/test-framework/data/512M.mp4",
	"/home/workspace/test-framework/data/1G.mp4",
	"/home/workspace/test-framework/data/2G.mp4",
	]

get_body = [
	"/32M",
	"/256M",
	"/512M",
	"/1G",
	"/2G",
	]

def trace(tag, msg):
	with open('./trace_log', 'a') as tracefile:
		tracefile.write(tag + msg)

def put(num):
	count = 100
	with open('./put_log' + str(num), 'w') as logfile:
		for body in put_body:
			run_cmd = "./poss {} --rpchost=192.168.50.233 --bucket={} --key={} --body={} --chiprice={} --expires={} --copies={}".format("put-object","testbucket","/obj"+str(num*10+count),body,"100","2018-12-30","1")
			print(run_cmd + "\n")
			time.sleep(random.randint(1,10))
			start_time = int(time.time())
			proc = subprocess.Popen(run_cmd,shell=True,stdout=logfile,stderr=logfile)
			proc.wait()
			end_time = int(time.time())
			msg = "start:{} -> stop:{}".format(str(start_time),str(end_time))
			trace("put:", msg)
			count += count

def get(num):
	with open('./get_log' + str(num), 'w') as logfile:
		for body in get_body:
			run_cmd = "./poss {} --rpchost=192.168.50.233 --bucket={} --key={} --outfile={} --chiprice={}".format("get-object","testbucket",body,"./tmp_download_file","100")
			print(run_cmd + "\n")
			time.sleep(random.randint(1,10))
			start_time = int(time.time())
			proc = subprocess.Popen(run_cmd,shell=True,stdout=logfile,stderr=logfile)
			proc.wait()
			end_time = int(time.time())
			msg = "start:{} -> stop:{}".format(str(start_time),str(end_time))
			trace("get:", msg)
			

pool = multiprocessing.Pool(processes = 3)

for i in xrange(10):
	rate = float(sys.argv[1])
	barrier = int(100 * rate)
	selector = random.randint(1,100)
	try:
		if selector < barrier:
        		pool.apply_async(put, (i, )) 
		elif selector >= barrier:
			pool.apply_async(get, (i, ))
	except Exception as e:
		print(e)

pool.close()
pool.join()
