import os,sys,time
import inspect
import json
import requests
import threading
import threadpool

class rpc(object):

    def __init__(self):
        self.headers = {"Content-Type": "text/json"} 
        self.timeout = 10
        self.internal = 3 
        self.tag = "rpc: || "

    def worker(self, url, headers, data):
        ret = None
        time.sleep(1)
        for i in range(5):
            try:
                response = requests.post(url, data = data, headers = headers, timeout = self.timeout)
                if(response.status_code == 200):
                    ret = response.text
                    break
                time.sleep(self.internal)
            except Exception as err:
                logger.info(self.tag + str(err),html=True,also_console=True)
        return ret
    
    def handle(self, ip, port, command, params, request_id):
        url = "http://{}:{}/rpc".format(ip,port)
        body = {"jsonrpc":"2.0","method":command,"params":params,"id":request_id}
        data = json.dumps(body)
        return self.worker(url, self.headers, data)

class node(object):

    def __init__(self, name, ip, port, tid):
        self.name = name
        self.ip = ip 
        self.port = port
        self.tid = tid
        self.request_id = 1
        self.rpc_handler = rpc()
        self.logfile = './' + name + "_" + str(self.tid) + '.log' 

    def tracer(self, pmethod, ptag, pmsg, ptime):
        with open(self.logfile, 'a') as tracefile:
            tracefile.write(pmethod + ":" + ptag + ":" + pmsg + ":" + str(ptime) + "\n")

    def wait_job_status(self, task, state, timeout=300):
        ret = None
        used_time = 0

        while used_time < timeout:
            start = int(time.time())
            time.sleep(3)

            status,ret = self.handle(command="GetJobProgress",params=[task])
            if(status == False and "Deleted" in state):
                return True,None
            elif(status == True and ret != None and ret["JobState"] in state):
                total_byete = float(ret["TotalBytes"])
                finished_byete = float(ret["FinishedBytes"])
                finished_rate = finished_byete / total_byete
                if(finished_rate >= float(finished)):
                    end = int(time.time())
                    used_time += end - start
                    return True,ret["ExResult"],used_time
            elif(status == True and ret != None and (ret["JobState"] == "Finished" or ret["JobState"] == "Error" or ("Err" in ret.keys() and len(ret["Err"]) > 0) or "Error" in ret.keys())):
                end = int(time.time())
                used_time += end - start
                return False,ret["ExResult"],used_time

            end = int(time.time())
            used_time += end - start

        return False, ret, used_time

    def handle(self, *args, **kargs):
        ret = {}

        command = kargs["command"]
        params = kargs["params"]

        #send http post request
        ret = self.rpc_handler.handle(self.ip, self.port, command, params, self.request_id)
        self.request_id += 1
        ret = ret.replace("\n","")
        ret = ret.replace("\\n","")
        ret = json.loads(ret)
        if("result" in ret.keys() and type(ret["result"]) == dict and "ExResult" in ret["result"].keys() and type(ret["result"]["ExResult"]) == str):
            tmp_str = ret["result"]["ExResult"]
            try:
                ret["result"]["ExResult"] = json.loads(ret["result"]["ExResult"])
            except Exception as err:
                ret["result"]["ExResult"] = tmp_str

        if("result" in ret.keys()):
            return True,ret["result"]
        return False,ret

    def get_object_status(self, bucket_name, key):
        ret = None
        status = False
        status,task = self.handle(command="ObjectStatus",params=[bucket_name, key])
        if(status == True and task != None):
            status,ret = self.wait_job_status(task, ["Finished"])
        return status,ret

    def wait_object_status(self, bucket_name, key, state, timeout=300):
        ret = None
        status = False

        used_time = 0
        while used_time < timeout:
            start = int(time.time())
            time.sleep(3)
            status,ret = self.get_object_status(bucket_name, key)
            end = int(time.time())
            used_time += end - start
            if("Deleted" in state and status == False):
                return True,None,used_time
            elif(status == True and ret != None and ret["state"] in state):
                return True,ret,used_time
            else:
                status = False
        return status,ret,used_time


###########################################################
commands = [
            {
                "command":"PutObject",
                "params":[]
            },
            {
                "command":"GetObject",
                "params":[]
            }
        ]
def run_test(name, ip, port, tid):
    user = node(name, ip, port, tid)
    for i in range(0,10):
        used_time = 0
        status,ret = user.handle(command="", params=[])
        if(status == True and ret != None):
            status,ret,used_time = user.wait_job_status(ret, ["Finished"], finished=0, timeout=300):
        else:
            user.tracer("put object", name, str(ret), used_time)
            continue

        if(status == True):
            user.tracer("put object", name, "success", used_time)
        else:
            user.tracer("put object", name, ret, used_time)

dict_vars_1 = {'a':'./log1.txt', 'b':'2'}
dict_vars_2 = {'a':'./log2.txt', 'b':'5'}
dict_vars_3 = {'a':'./log3.txt', 'b':'5'}
var = [(None, dict_vars_1), (None, dict_vars_2), (None, dict_vars_3)]

pool = threadpool.ThreadPool(2)
requests = threadpool.makeRequests(func, var)

[pool.putRequest(req) for req in requests]

pool.wait()
