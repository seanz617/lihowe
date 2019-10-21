import os,sys,time,datetime
from robot.api import logger
from test_config import test_config
from base import base
from ppio import ppio

class test_ppio(base):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        base.__init__(self, self.__class__.__name__)

    def import_object(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","ppio0")
        expect = dict_param.get("result", True)
        fpath = dict_param.get("path", "")
        if fpath != "" and fpath.find("/") < 0:
            fpath = "{}/{}".format(test_config.get_config("file_repo"),fpath)

        status, ret = self.handle(ppio, operator, "import_object")(fpath)
        assert expect == status, "import_object failed"
        return ret if expect else None

    def export_object(self, dict_param, chunks=None):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","ppio0")
        expect = dict_param.get("result", True)
        outfile = dict_param.get("outfile","file.tmp")
        if outfile.find("/") < 0:
            outfile = "{}/{}".format(test_config.get_config("tmp_dir"),outfile)

        list_param = [
                chunks["Hash"] if chunks else dict_param.get("hash", None),
                outfile 
                ]
        assert expect == self.handle(ppio, operator, "export_object")(list_param)[0] and os.path.exists(outfile),"export_object failed"

    def delete_object(self, dict_param, chunks=None):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","ppio0")
        expect = dict_param.get("result", True)
        object_hash = chunks["Hash"] if chunks else dict_param.get("hash", None)

        assert expect == self.handle(ppio, operator, "delete_object")([object_hash])[0], "delete_object failed"

    def put_chunks(self, dict_param, chunks=None):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","ppio0")
        expect = dict_param.get("result", True)
        sync = dict_param.get("sync", True)
        chunk_infos = chunks["Chunks"] if chunks else dict_param.get("chunks", [])

        time_limit = self.get_time_limit("put", 1, int(dict_param.get("copies", 1)))

        for c in chunk_infos: 
            list_param = [c["Hash"],
                    dict_param.get("chiprice","200"),
                    int(dict_param.get("copies", 1)),
                    dict_param.get("duration", 86400)
                    ]
            assert expect == self.handle(ppio, operator, "put_chunk", time_limit)(list_param)[0], "put_chunk failed"
        
            if sync and expect:
                #chunk_list = [c["Hash"] for c in chunk_infos]
                #assert self.handle(ppio, operator, "wait_chunk_status")(chunk_list)[0]
                assert self.handle(ppio, operator, "wait_chunk_status")([c["Hash"]])[0], "wait_chunk_status failed"

    def get_chunks(self, dict_param, chunks=None):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","ppio0")
        expect = dict_param.get("result", True)
        chunk_infos = chunks["Chunks"] if chunks else dict_param.get("chunks", [])

        time_limit = self.get_time_limit("get", 1)

        for c in chunk_infos: 
            list_param = [c["Hash"], 
                    dict_param.get("chiprice","200")
                    ]
            assert expect == self.handle(ppio, operator, "get_chunk", time_limit)(list_param)[0]

    def delete_chunks(self, dict_param, chunks=None):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","ppio0")
        expect = dict_param.get("result", True)
        check_miner = dict_param.get("check_miner", False)
        chunk_infos = chunks["Chunks"] if chunks else dict_param.get("chunks", [])

        for c in chunk_infos: 
            assert expect == self.handle(ppio, operator, "delete_chunk")([c["Hash"]])[0]

        time.sleep(self.get_time_limit("delete", len(chunk_infos)))

        chunk_list = [c["Hash"] for c in chunk_infos]
        status, ret = self.handle(ppio, operator, "get_chunk_status")(chunk_list)
        if status and ret:
            for r in ret:
                for contract in r["Contracts"]:
                    assert contract["Status"] != "SC_AVAILABLE"

        if check_miner:
            pass

    def renew_chunks(self, dict_param, chunks=None):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","ppio0")
        expect = dict_param.get("result", True)
        sync = dict_param.get("sync", True)
        duration_buffer = dict_param.get("duration_buffer", 5)
        chunk_infos = chunks["Chunks"] if chunks else dict_param.get("chunks", [])
        chunk_list = [c["Hash"] for c in chunk_infos]

        status, ret = self.handle(ppio, operator, "get_chunk_status")(chunk_list)
        assert len(ret) == len(chunk_list)

        time_limit = self.get_time_limit("renew", len(chunk_list), int(dict_param.get("copies", 1)))

        for chunk in ret: 
            begin_time = 0 
            expire_time = 0
            for contract in chunk["Contracts"]:
                begin_time = contract["BeginTime"] if begin_time < contract["BeginTime"] else begin_time
                expire_time = contract["ExpireTime"] if expire_time < contract["ExpireTime"] else expire_time
            duration = expire_time - begin_time

            current = int(time.time())
            new_duration = dict_param.get("duration", 86400)
            if duration - duration_buffer <= new_duration <= duration + duration_buffer:
                new_duration = duration - current + begin_time + duration_buffer

            list_param = [chunk["Hash"],
                    dict_param.get("chiprice", "200"),
                    dict_param.get("copies", 1),
                    new_duration if new_duration >= 86400 else 86400
                    ]
            assert expect == self.handle(ppio, operator, "renew_chunk", time_limit)(list_param)[0]

        if sync and expect:
            chunk_list = [c["Hash"] for c in chunk_infos]
            assert self.handle(ppio, operator, "wait_chunk_status")(chunk_list)[0]

    def clear_chunks(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","ppio0")
        assert self.handle(ppio, operator, "clear_chunk")([])[0]

    def check_chunks_status(self, dict_param, chunks=None):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","ppio0")
        chunk_infos = chunks["Chunks"] if chunks else dict_param.get("chunks", [])
        chunk_list = [c["Hash"] for c in chunk_infos]
        assert expect == self.handle(ppio, operator, "get_chunk_status")(chunk_list, dict_param.get("chiprice","200"), dict_param.get("copies", 1), dict_param.get("duration", 86400))[0]

if __name__ == "__main__":
    pass
