import os,sys,time
from robot.api import logger
from test_config import test_config
from miner import miner
from base import base 
from poss import poss

class test_poss(base):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        base.__init__(self, self.__class__.__name__)

    def create_bucket(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        bucket = dict_param.get("bucket","tstbucket")
        expect = dict_param.get("result",True)

        assert expect == self.handle(poss, operator, "create_bucket")([bucket])[0], "create bucket fail"

        if expect:
            status, ret = self.handle(poss, operator, "list_buckets")()
            assert status and bucket in ret, 'list buckets fail'

    def delete_bucket(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        bucket = dict_param.get("bucket","tstbucket")
        expect = dict_param.get("result",True)
        delete_objects_flag = dict_param.get("delete_objects", False)

        if expect and delete_objects_flag:
            status, objs = self.handle(poss, operator, "list_objects")(bucket)
            assert status
            for obj in objs:
                assert self.handle(poss, operator, "delete_object")([bucket, obj["key"]])[0]

        assert expect == self.handle(poss, operator, "delete_bucket")([bucket])[0]

    def put_object(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        expect = dict_param.get("result", True)
        sync = dict_param.get("sync",True)
        bucket = dict_param.get("bucket","tstbucket")
        isdir = dict_param.get("isdir", False)
        check_miner = dict_param.get("check_miner", False)
        
        body = dict_param.get("body","") 
        chunks = 0
        if isdir:
            body = ""
            chunks = 0
        elif body != "" and body.find("/") < 0:
            body = "{}/{}".format(test_config.get_config("file_repo"),body)
            if os.path.exists(body):
                chunks = ( os.path.getsize(body) >> 24 ) + 1
            else:
                assert False == expect, "file not dound"

        copies = 1
        try:
            copies = int(dict_param.get("copies","1"))
        except Exception as err:
            copies = dict_param.get("copies","1")

        time_limit = self.get_time_limit("put", chunks, copies)

        status, ret = self.handle(poss, operator, "list_buckets")()
        assert status, "list_buckets failed"
        if not ret or bucket not in ret:
            assert self.handle(poss, operator, "create_bucket")([bucket])[0], "create bucket failed"

        list_param = [
                dict_param.get("bucket","tstbucket"),
                dict_param.get("key",""),
                body,
                dict_param.get("meta",""),
                dict_param.get("chiprice","200"),
                #int(dict_param.get("copies","1")),
                copies,
                dict_param.get("expires","2019-12-31"),
                dict_param.get("encrypt",True)
                ]
        status, ret = self.handle(poss, operator, "put_object", time_limit)(list_param, sync)
        assert status == expect, "put_object failed" + str(status) + str(expect)

        if expect and sync and check_miner: 
            assert ret, 'put_object return nothing'
            for chunk in ret["contracts"]:
                chunk_hash = chunk["Hash"]
                for contract in chunk["Contracts"]:
                    if contrace["Status"] == "SC_AVAILABLE":
                        miner_id = contract["MinerID"]
                        miner_name, _ = test_config.get_miner_by_id(miner_id)
                        s, r = self.handle(miner, miner_name, "chunk_info")()
                        assert s and r, "check miner chunk failed"

        return ret if expect else None

    def get_object(self, dict_param, share_code=""):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        expect = dict_param.get("result", True)
        sync = dict_param.get("sync",True)
        outfile = dict_param.get("outfile","file.tmp")
        if outfile.find("/") < 0:
            outfile = "{}/{}".format(test_config.get_config("tmp_dir"),outfile)

        time_limit = self.get_time_limit("get")

        list_param = [
                dict_param.get("bucket","tstbucket"),
                dict_param.get("key",""),
                dict_param.get("sharecode","") if share_code == "" else share_code,
                outfile,
                dict_param.get("chiprice","200")
                ]
        status, ret = self.handle(poss, operator, "get_object", time_limit)(list_param, sync) 
        if sync:
            assert expect == (status and os.path.exists(outfile))
        else:
            assert expect == status 
        return ret if expect else None

    def delete_object(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        expect = dict_param.get("result", True)
        check_miner = dict_param.get("check_miner", False)
        bucket = dict_param.get("bucket","tstbucket")
        key = dict_param.get("key","")
        isdir = dict_param.get("isdir",False)

        list_param = [
                dict_param.get("bucket","tstbucket"),
                dict_param.get("key","")
                ]

        if not isdir:
            status, chunk_infos = self.handle(poss, operator, "get_object_status")(bucket,key)
            assert expect == status 

        assert expect == self.handle(poss, operator, "delete_object")(list_param)[0]

        if expect and check_miner:
            time.sleep(self.get_time_limit("delete"))
            for chunk in chunk_infos["contracts"]:
                chunk_hash = chunk["Hash"]
                for contract in chunk["Contracts"]:
                    miner_id = contract["MinerID"]
                    miner_name, _ = test_config.get_miner_by_id(miner_id)
                    status, ret = self.handle(miner, miner_name, "chunk_info")()
                    assert not status

    def share_object(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        expect = dict_param.get("result", True)

        list_param = [
                dict_param.get("bucket","tstbucket"),
                dict_param.get("key","")
                ]
        status, sharecode = self.handle(poss, operator, "share_object")(list_param)
        assert expect == status 
        return sharecode if expect else None

    def renew_object(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        expect = dict_param.get("result", True)
        sync = dict_param.get("sync", True)

        copies = 1
        try:
            copies = int(dict_param.get("copies","1"))
        except Exception as err:
            copies = dict_param.get("copies","1")

        time_limit = self.get_time_limit("renew", 0, copies)

        list_param = [
                dict_param.get("bucket","tstbucket"),
                dict_param.get("key",""),
                dict_param.get("chiprice","200"),
                copies,
                dict_param.get("expires","2020-01-01")
                ]
        assert expect == self.handle(poss, operator, "renew_object", time_limit)(list_param, sync)[0]

    def copy_object(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        expect = dict_param.get("result", True)
        sync = dict_param.get("sync", True)

        bucket = dict_param.get("bucket","tstbucket")
        status, ret = self.handle(poss, operator, "list_buckets")()
        assert status
        if not ret or bucket not in ret:
            assert self.handle(poss, operator, "create_bucket")([bucket])[0]

        time_limit = self.get_time_limit("renew", 0, int(dict_param.get("copies","1")))

        list_param = [
                dict_param.get("bucket","tstbucket"),
                dict_param.get("key",""),
                dict_param.get("source",""),
                dict_param.get("meta", ""),
                dict_param.get("chiprice","200"),
                int(dict_param.get("copies","1")),
                dict_param.get("expires","2019-12-21"),
                dict_param.get("encrypt", True)
            ]
        status, ret = self.handle(poss, operator, "copy_object", time_limit)(list_param, sync)
        assert expect == status
        return ret if expect else None

    def move_object(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        expect = dict_param.get("result", True)
        sync = dict_param.get("sync", True)
        bucket = dict_param.get("bucket","tstbucket")

        status, ret = self.handle(poss, operator, "list_buckets")()
        assert status
        if not ret or bucket not in ret:
            assert self.handle(poss, operator, "create_bucket")([bucket])[0]
                
        list_param = [
                dict_param.get("bucket","tstbucket"),
                dict_param.get("key",""),
                dict_param.get("source","")
                ]
        assert expect == self.handle(poss, operator, "move_object")(list_param)[0]

    def check_object_status(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        expect = dict_param.get("result", True)
        bucket = dict_param.get("bucket","tstbucket")
        key = dict_param.get("key","")
        state = dict_param.get("state","Deal")

        assert expect == self.handle(poss, operator, "wait_object_status")(bucket, key, [state])[0]
        if expect and state == "Deal":
            assert self.handle(poss, operator, "check_object_status")(bucket, key, int(dict_param.get("chiprice","200")), int(dict_param.get("copies","1")), dict_param.get("expires","2019-12-31"))[0]
    
    def pause_task(self, dict_param, task):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        expect = dict_param.get("result", True)
        condition = dict_param.get("condition",0.0)/100.0

        assert expect == self.handle(poss, operator, "pause_task")(task, condition)[0]
            
    def resume_task(self, dict_param, task):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        expect = dict_param.get("result", True)
        sync = dict_param.get("sync", True)

        assert expect == self.handle(poss, operator, "resume_task")(task)[0]
        if expect and sync: 
            assert self.handle(poss, operator, "wait_job_status")(task, ["Finished"])[0]

    def delete_task(self, dict_param, task):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","poss0")
        assert expect == self.handle(poss, operator, "delete_task")(task)[0]

if __name__ == "__main__":
    pass
