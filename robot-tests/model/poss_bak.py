import os,sys,time
import math
from robot.api import logger
import json
from node import node

class poss(node):

    def __init__(self, name):
        node.__init__(self, name)

    #-----------bucket operations------------
    def list_buckets(self):
        return self.handle(command="ListBuckets",params=[])

    def create_bucket(self, bucket_name):
        #create bucket
        status, ret = self.handle(command="CreateBucket",params=[bucket_name])

        #search bucket
        if(status == True):
            status,ret = self.list_buckets()

        if(status == True and bucket_name in ret):
            return True,ret
        return False,ret

    def delete_bucket(self, bucket_name, timeout=30):
        if(timeout == ""):
            timeout = self.default["object_available_timeout"]
        #delete object in bucket
        status,ret = self.list_objects(bucket_name)
        if(status == True and ret != None and len(ret) > 0):
            for obj_iter in ret:
                self.delete_object(bucket_name,obj_iter["key"], timeout)

        #delete bucket
        status,ret = self.handle(command="DeleteBucket",params=[bucket_name])
        if(status == True):
            status,ret = self.list_buckets()

        if(status == True and (ret == None or bucket_name not in ret)):
            return True,ret
        return False,ret

    #----------job operations-------------
    def get_job(self, task):
        status,ret = self.handle(command="GetJobProgress",params=[task])
        if(status == True and ret != None):
            return True,ret["ExResult"]
        return status,ret

    def wait_job_status(self, task, state, finished=0, timeout=""):

        if(timeout == ""):
            timeout = self.default["task_finish_timeout"]
        
        ret = None
        used_time = 0

        while used_time < timeout:
            start = int(time.time())
            if(self.parallel == False):
                time.sleep(3)

            status,ret = self.handle(command="GetJobProgress",params=[task])
            if(status == False and "Deleted" in state):
                return True,None
            elif(status == True and ret != None and ret["JobState"] in state):
                total_byete = float(ret["TotalBytes"])
                finished_byete = float(ret["FinishedBytes"])
                finished_rate = finished_byete / total_byete
                if(finished_rate >= float(finished)):
                    return True,ret["ExResult"]
            elif(status == True and ret != None and (ret["JobState"] == "Finished" or ret["JobState"] == "Error" or ("Err" in ret.keys() and len(ret["Err"]) > 0) or "Error" in ret.keys())):
                return False,ret["ExResult"]

            end = int(time.time())
            used_time += end - start

        return False, ret

    #----------task operations------------
    def list_tasks(self):
        return self.handle(command="ListTasks",params=[])

    def pause_task(self, task, timeout):
        #wait task created
        status,ret = self.wait_job_status(task, ["Running"])
    
        #pause task
        if(status == True and ret["JobState"] == ["Running"]):
            status,ret = self.handle(command="PauseTask",params=[task])

        #find task and check task state
        if(status == True):
            status,ret = self.wait_job_status(task,["Paused"])
        return status,ret

    def pause_task_by_condition(self, task, condition, timeout):
        status = False
        ret = None
        used_time = 0

        #check task running
        status,ret = self.wait_job_status(task, ["Running"], condition)

        #pause task
        if(status == True):
            status,ret = self.handle(command="PauseTask",params=[task])

        #wait task paused
        if(status == True):
            status,ret = self.wait_job_status(task, ["Paused"])

        return status,ret

    def resume_task(self, task, timeout):
        #resume task
        status,ret = self.handle(command="ResumeTask",params=[task])

        #check task running or finished
        if(status == True):
            status,ret = self.wait_job_status(task, ["Running", "Finished"])

        return status,ret

    def delete_task(self, task, timeout=""):
        #delete task
        status,ret = self.handle(command="DeleteTask",params=[task])

        #wait task deleted
        #if(status == True):
        #    status,ret = self.wait_job_status(task, ["Deleted"], 0, 90)

        return status,ret

    #-----------object operations------------
    def list_objects(self, bucket_name):
        return self.handle(command="ListObjects",params=[bucket_name])

    def find_object(self, bucket_name, key):
        #list objects
        status,keys = self.list_objects(bucket_name) 
        if(status == True and (keys == None or len(keys) <= 0)):
            return False,None
        elif(status == True and type(keys) == list):
            #search object
            for key_iter in keys:
                if(key_iter["key"] == key):
                    return True,key_iter
            return False,None
        return False,"error:list objects failed"

    def delete_object_p(self, params):
        #delete object
        status,ret = self.handle(command="DeleteObject",params=params)
        bucket_name = params[0]
        key = params[1]

        #wait object deleted
        if(status == True):
            status,ret = self.wait_object_status(bucket_name, key, ["Deleted"])

        return status,ret

    def delete_object(self, bucket_name, key, timeout=""):
        if(timeout == ""):
            timeout = self.default["object_available_timeout"]

        #delete object
        status,ret = self.handle(command="DeleteObject",params=[bucket_name, key])

        #wait object deleted
        if(status == True):
            status,ret = self.wait_object_status(bucket_name, key, ["Deleted"])

        return status,ret

    def put_object_p(self, params):

        bucket_name = params[0]
        key = params[1]
        chiprice = params[4]
        copies = params[5]
        expires = params[6]
        #put object
        status,ret = self.handle(command="PutObject",params=params)
        task = ret

        #wait task finish 
        if(status == True and ret != None):
            status,ret = self.wait_job_status(task, ["Finished"])

        self.delete_task(task)

        #wait object available
        if(status == True):
            status,ret = self.wait_object_status(bucket_name, key, ["Deal"])

        #check object status details
        if(status == True):
            status,ret = self.check_object_status(bucket_name, key, chiprice, copies, expires, ret)
        return status,task

    def put_object(self, 
                    bucket_name, 
                    key, 
                    body, 
                    meta, 
                    chiprice, 
                    copies, 
                    expires, 
                    encrypt, 
                    sync, 
                    task_finish_timeout, 
                    object_available_timeout):
        if(meta == ""):
            meta = self.default["meta"]
        if(chiprice == ""):
            chiprice = self.default["chiprice"]
        if(copies == ""):
            copies = self.default["copies"]
        if(expires == ""):
            expires = self.default["expires"]
        if(encrypt == ""):
            encrypt = self.default["encrypt"]
        if(sync == ""):
            sync = self.default["sync"]
        if(task_finish_timeout == ""):
            task_finish_timeout = self.default["task_finish_timeout"]
        if(object_available_timeout == ""):
            object_available_timeout = self.default["object_available_timeout"]

        #if bucket not exists then create bucket
        status,ret = self.list_buckets()
        if(status == False):
            return False,{}
        if(status == True and (ret == None or bucket_name not in ret)):
            status,ret = self.create_bucket(bucket_name)
            if(status == False):
                return False,ret

        #if object exists then delete object
        status,ret = self.find_object(bucket_name,key)
        if(status == True and ret != None):
            status,ret = self.delete_object(bucket_name,key)
            if(status == False or ret != None):
                return False,ret

        #put object
        params = [bucket_name, key, body, meta, chiprice, copies, expires, encrypt]
        status,ret = self.handle(command="PutObject",params=params)
        task = ret

        #put directory
        if(status == True and body == ""):
            status,ret = self.list_objects(bucket_name)
            if(status == True):
                for obj_iter in ret:
                    if(obj_iter["key"] == key and obj_iter["isdir"] == True):
                        status = True
            else:
                status = False 
            return status,ret
        
        #sync wait
        if(sync == True):
            time.sleep(3)

            #wait task finish 
            if(status == True and ret != None):
                status,ret = self.wait_job_status(task, ["Finished"])
            else:
                logger.info("task not found", html=True, also_console=True)

            #wait object available
            if(status == True):
                status,ret = self.wait_object_status(bucket_name, key, ["Deal"])
            else:
                logger.info("delete task failed", html=True, also_console=True)

            #check object status details
            if(status == True):
                status,ret = self.check_object_status(bucket_name, key, chiprice, copies, expires, ret)
            else:
                logger.info("object status wrong", html=True, also_console=True)
        elif(status == True):
            status,ret = self.wait_job_status(task, ["Running"])
        return status,task

    def get_object_status(self, bucket_name, key):
        ret = None
        status = False
        status,task = self.handle(command="ObjectStatus",params=[bucket_name, key])
        if(status == True and task != None):
            status,ret = self.wait_job_status(task, ["Finished"])
            self.delete_task(task)
        return status,ret

    def check_object_status(self, bucket_name, key, chiprice, copies, expires, obj_status=""):
        if(chiprice == ""):
            chiprice = self.default["chiprice"]
        if(copies == ""):
            copies = self.default["copies"]
        if(expires == ""):
            expires = self.default["expires"]

        ret = None
        status = False

        #get object status
        status,ret = self.get_object_status(bucket_name, key)
                
        if(status == True ):
            #check state
            state = ret["state"]
            if(state != "Deal"):
                return False,ret

            #check chunk num
            chunk_num = int(ret["length"] / 16777216) + 1
            contracts = ret["contracts"]
            if(len(contracts) != chunk_num):
                return False,ret

            #check contract num and contract status
            for chunk in contracts:
                contract_count = 0
                for contract in chunk["Contracts"]:
                    if(contract["Status"] == "SC_AVAILABLE"):
                        contract_count += 1
                        if(contract["UserChiPrice"] != chiprice):
                            return False,ret
                if(contract_count != int(copies)):
                    return False,ret

        return status,ret

    def wait_object_status(self, bucket_name, key, state, timeout=""):
        ret = None
        status = False

        if(timeout == ""):
            timeout = self.default["object_available_timeout"]

        used_time = 0
        while used_time < timeout:
            start = int(time.time())
            if(self.parallel == False):
                time.sleep(3)
            status,ret = self.get_object_status(bucket_name, key)
            if("Deleted" in state and status == False):
                return True,None
            elif(status == True and ret != None and ret["state"] in state):
                return True,ret
            else:
                status = False
            end = int(time.time())
            used_time += end - start

        return status,ret
 
    def get_object_p(self, params):
        #get object
        status,ret = self.handle(command="GetObject",params=params)
        task = ret
           
        #wait task finish 
        if(status == True and ret != None):
            status,ret = self.wait_job_status(task, ["Finished"])

        self.delete_task(task)

        return status, task

    def get_object(self, 
                    bucket_name, 
                    key, 
                    sharecode, 
                    outfile, 
                    chiprice, 
                    sync, 
                    task_finish_timeout):
        if(chiprice == ""):
            chiprice = self.default["chiprice"]
        if(outfile == ""):
            outfile = self.default["outfile"]
        if(sync == ""):
            sync = self.default["sync"]
        if(task_finish_timeout == ""):
            task_finish_timeout = self.default["task_finish_timeout"]

        #get object
        params = [bucket_name, key, sharecode, outfile, chiprice]
        status,ret = self.handle(command="GetObject",params=params)
        task = ret
           
        if(sync == True):
            time.sleep(3)

            #wait task finish 
            if(status == True and ret != None):
                status,ret = self.wait_job_status(task, ["Finished"])
        elif(status == True):
            status,ret = self.wait_job_status(task, ["Running"])
        return status, task

    def head_object(self, bucket_name, key):
        return self.handle(command="HeadObject",params=[bucket_name, key])

    def get_job_progress(self, task):
        return self.handle(command="GetJobProgress",params=[task])

    def share_object(self, bucket_name, key):
        return self.handle(command="ShareObject",params=[bucket_name, key])

    def copy_object(self, 
                    bucket_name, 
                    key, 
                    source, 
                    meta, 
                    chiprice, 
                    copies, 
                    expires, 
                    encrypt,
                    sync, 
                    task_finish_timeout, 
                    object_available_timeout):
        
        if(meta == ""):
            meta = self.default["meta"]
        if(chiprice == ""):
            chiprice = self.default["chiprice"]
        if(copies == ""):
            copies = self.default["copies"]
        if(expires == ""):
            expires = self.default["expires"]
        if(encrypt == ""):
            encrypt = self.default["encrypt"]
        if(sync == ""):
            sync = self.default["sync"]
        if(task_finish_timeout == ""):
            task_finish_timeout = self.default["task_finish_timeout"]
        if(object_available_timeout == ""):
            object_available_timeout = self.default["object_available_timeout"]

        status = False
        ret = None

        #if bucket not exists then create bucket
        status,ret = self.list_buckets()
        if(status == False):
            return False,{}
        if(status == True and (ret == None or bucket_name not in ret)):
            status,ret = self.create_bucket(bucket_name)
            if(status == False):
                return False,ret

        #copy object
        params = [bucket_name, key, source, meta, chiprice, copies, expires, encrypt]
        status,ret = self.handle(command="CopyObject",params=params)
        task = ret

        if(sync == True):
            time.sleep(3)

            #wait task finish 
            if(status == True and ret != None):
                status,ret = self.wait_job_status(task, ["Finished"])

            #wait object available
            if(status == True):
                status,ret = self.wait_object_status(bucket_name, key, ["Deal"])

            #check object status details
            if(status == True):
                status,ret = self.check_object_status(bucket_name, key, chiprice, copies, expires)
        elif(status == True):
            status,ret = self.wait_job_status(task, ["Running"])

        return status,task

    def renew_object(self, 
                    bucket_name, 
                    key, 
                    chiprice, 
                    copies, 
                    expires, 
                    sync,
                    task_finish_timeout,
                    object_available_timeout):
        status = False
        ret = None

        if(chiprice == ""):
            chiprice = self.default["chiprice"]
        if(copies == ""):
            copies = self.default["copies"]
        if(expires == ""):
            expires = self.default["expires"]
        if(sync == ""):
            sync = self.default["sync"]
        if(task_finish_timeout == ""):
            task_finish_timeout = self.default["task_finish_timeout"]
        if(object_available_timeout == ""):
            object_available_timeout = self.default["object_available_timeout"]

        #renew object
        params = [bucket_name, key, chiprice, copies, expires]
        status,ret = self.handle(command="RenewObject",params=params)
        task = ret

        if(sync == True):
            time.sleep(3)
   
            #wait task finish
            if(status == True):
                status,ret = self.wait_job_status(task, ["Finished"])

            #wait renew object finish
            if(status == True):
                status,ret = self.wait_object_status(bucket_name, key, ["Deal"])

            #check object status details
            if(status == True):
                status,ret = self.check_object_status(bucket_name, key, chiprice, copies, expires)

        return status,ret

       
    def move_object(self, bucket_name, key, move_source):
        return self.handle(command="MoveObject",params=[bucket_name, key, move_source])

    def export_root_hash(self):
        pass

    def import_root_hash(self):
        pass

    def import_wallet_key(self):
        pass

if __name__ == "__main__":
    #obj = poss("user1")
    #status, ret = obj.wait_job_status("",["Finished"])
    #status, ret = obj.put_object_p([""])
    pass
   
