import os,sys,time
import math
import json
from robot.api import logger
from node import node

class poss(node):

    def __init__(self, name):
        node.__init__(self, name)

    #-----------bucket operations------------
    def list_buckets(self):
        return self.handle(command="ListBuckets",params=[])

    def create_bucket(self, params):
        if self.handle(command="CreateBucket",params=params)[0]:
            status, buckets = self.list_buckets()
            if status and params[0] in buckets:
                return True, None 
        return False, None 

    def delete_bucket(self, params):
        if self.handle(command="DeleteBucket",params=params)[0]:
            status, buckets = self.list_buckets()
            if status and (not buckets or params[0] not in buckets):
                return True, None 
        return False, None

    #----------job operations-------------
    def get_job(self, task):
        status,ret = self.handle(command="GetJobProgress",params=[task])
        if status and ret:
            return True, ret["ExResult"]
        return status, ret

    def wait_job_status(self, task, state, finished=0.0, timeout=180):
        ret = None
        used_time = 0
        start = int(time.time())
        while used_time < timeout:
            time.sleep(1)
            status,ret = self.handle(command="GetJobProgress",params=[task])
            if not status and "Deleted" in state:
                return True, None
            elif not status:
                return False, None

            if status and ret and ret["JobState"] in state:
                if( (float(ret["TotalBytes"]) / float(ret["FinishedBytes"])) >= finished):
                    return True, ret["ExResult"]
            elif(status and ret and (ret["JobState"] == "Finished" or ret["JobState"] == "Error" or ("Err" in ret.keys() and len(ret["Err"]) > 0) or "Error" in ret.keys())):
                return False, ret["ExResult"]
            used_time = int(time.time()) - start
        return False, ret

    #----------task operations------------
    def list_tasks(self):
        return self.handle(command="ListTasks",params=[])

    def pause_task(self, task, condition=0.0):
        status, ret = self.wait_job_status(task, ["Running"], condition)
        if status:
            if self.handle(command="PauseTask",params=[task])[0]:
                return self.wait_job_status(task,["Paused"])
        return status, ret 

    def resume_task(self, task):
        status, ret = self.handle(command="ResumeTask",params=[task])
        if status:
            return self.wait_job_status(task, ["Running", "Finished"])
        return status, ret

    def delete_task(self, task):
        return self.handle(command="DeleteTask",params=[task])

    #-----------object operations------------
    def list_objects(self, bucket):
        return self.handle(command="ListObjects",params=[bucket])

    def find_object(self, bucket, key):
        status, keys = self.list_objects(bucket) 
        if status and (not keys or len(keys) <= 0):
            return False, keys
        elif status and type(keys) == list:
            for k in keys:
                if(k["key"] == key):
                    return True, k
        return False, "object not found"

    def delete_object(self, params):
        if self.handle(command="DeleteObject",params=params)[0]:
            return self.wait_object_status(params[0], params[1], ["Deleted"])
        return False,"delete object fail"

    def put_object(self, params, sync=True): 
        status,task = self.handle(command="PutObject",params=params)
        #put directory
        if status and not params[2]:
            status, ret = self.list_objects(params[0])
            if status:
                for obj_iter in ret:
                    if(obj_iter["key"] == params[1] and obj_iter["isdir"] == True):
                        return True, ret 
            return False, ret
        
        if sync and status:
            time.sleep(3)
            status, ret = self.wait_job_status(task, ["Finished"])
            if status:
                status, ret = self.wait_object_status(params[0], params[1], ["Deal"])
            if status:
                status, ret = self.check_object_status(params[0], params[1], params[4], params[5], params[6])
            return status, ret
        elif status:
            status, _ = self.wait_job_status(task, ["Running"])
            return status, task
        return False, None

    def get_object_status(self, bucket, key):
        ret = None
        status,task = self.handle(command="ObjectStatus",params=[bucket, key])
        if status and task:
            status, ret = self.wait_job_status(task, ["Finished"])
            self.delete_task(task)
        return status, ret

    def check_object_status(self, bucket, key, chiprice, copies, expires):
        status,ret = self.get_object_status(bucket, key)
        if status:
            if ret["state"] != "Deal":
                return False, ret

            chunk_num = int(ret["length"] / 16777216) + 1
            contracts = ret["contracts"]
            if(len(contracts) != chunk_num):
                return False, ret

            for chunk in contracts:
                contract_count = 0
                for contract in chunk["Contracts"]:
                    if(contract["Status"] == "SC_AVAILABLE"):
                        contract_count += 1
                        if(int(contract["UserChiPrice"]) != int(chiprice)):
                            return False, ret
                if(contract_count != int(copies)):
                    return False, ret
        return status, ret

    def wait_object_status(self, bucket, key, state, timeout=180):
        ret = None
        used_time = 0
        start = int(time.time())
        while used_time < timeout:
            time.sleep(1)
            status,ret = self.get_object_status(bucket, key)
            if "Deleted" in state and not status:
                return True, None
            elif status and ret and ret["state"] in state:
                return True, ret
            used_time = int(time.time()) - start
        return False, ret
 
    def get_object(self, params, sync=True):
        status, task = self.handle(command="GetObject",params=params)
        if sync and status and task:
            time.sleep(3)
            status, ret = self.wait_job_status(task, ["Finished"])
            return status, ret
        elif status and task:
            time.sleep(3)
            status, _ = self.wait_job_status(task, ["Running"])
            return status, task
        return False, None

    def head_object(self, bucket, key):
        return self.handle(command="HeadObject",params=[bucket_name, key])

    def get_job_progress(self, task):
        return self.handle(command="GetJobProgress",params=[task])

    def share_object(self, params):
        return self.handle(command="ShareObject",params=params)

    def copy_object(self, params, sync=True):
        status, task = self.handle(command="CopyObject",params=params)
        if sync and status and task:
            time.sleep(3)
            status, ret = self.wait_job_status(task, ["Finished"])
            if status:
                status, ret = self.wait_object_status(params[0], params[1], ["Deal"])
            if status:
                status, ret = self.check_object_status(params[0], params[1], params[4], params[5], params[6])
            return status, ret
        elif status and task:
            status, _ = self.wait_job_status(task, ["Running"])
            return status, task
        return False, None

    def renew_object(self, params, sync=True):
        status, task = self.handle(command="RenewObject",params=params)
        if sync and status and task:
            time.sleep(3)
            status, ret = self.wait_job_status(task, ["Finished"])
            if status:
                status, ret = self.wait_object_status(params[0], params[1], ["Deal"])
            if status:
                status, ret = self.check_object_status(params[0], params[1], params[2], params[3], params[4])
            return status, ret
        elif status and task:
            status, _ = self.wait_job_status(task, ["Running"])
            return status, task
        return False, None
       
    def move_object(self, params):
        return self.handle(command="MoveObject",params=params)

    def export_root_hash(self):
        pass

    def import_root_hash(self):
        pass

    def import_wallet_key(self):
        pass

if __name__ == "__main__":
    pass
