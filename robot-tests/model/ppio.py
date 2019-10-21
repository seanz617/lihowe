import os, sys, time, re, math
from robot.api import logger
from node import node


class ppio(node):

    def __init__(self, name):
        node.__init__(self, name)

    def import_object(self, path):
        fsize = os.path.getsize(path)
        chunk_num = int(fsize / 16777216) + 1 if fsize > 0 else 0
        _, ret = self.handle(command="ObjectImport", params=[path])
        if ret and (len(ret["Chunks"]) == chunk_num or len(ret["Chunks"]) == chunk_num + 1):
            return True, ret
        return False, ret

    def export_object(self, params):
        status, ret = self.handle(command="ObjectExport", params=params)
        return status, ret

    def delete_object(self, params):
        return self.handle(command="ObjectDelete", params=params)

    def put_chunk(self, params):
        status, ret = self.handle(command="ChunkPut", params=params)
        time.sleep(5)
        return status, ret

    def get_chunk(self, params):
        return self.handle(command="ChunkGet", params=params)

    def delete_chunk(self, params):
        return self.handle(command="ChunkDelete", params=params)

    def get_chunk_status(self, chunk_hash, chiprice=0, copies=0, duration=0):
        status, ret = self.handle(command="ChunkStatus", params=[chunk_hash])
        if chiprice == 0 and copies == 0 and duration == 0:
            return status, ret

        if status and len(ret) > 0:
            for r in ret:
                available_count = 0
                for c in r["Contracts"]:
                    if (c["Status"] == "SC_AVAILABLE" and int(c["UserChiPrice"]) == int(chiprice)):
                        available_count += 1
                if available_count != int(copies):
                    return False, ret
            return True, ret
        return False, ret

    def clear_chunk(self):
        return self.handle(command="ChunkClear", params=[])

    def renew_chunk(self, params):
        status, ret = self.handle(command="ChunkRenew", params=params)
        time.sleep(3)
        return status, ret

    def wait_chunk_status(self, chunk_hash, state=["SC_AVAILABLE", "SC_END"], timeout=180):
        ret = None
        used_time = 0
        start = int(time.time())
        while used_time < timeout:
            time.sleep(1)
            status, ret = self.handle(command="ChunkStatus", params=[chunk_hash])
            if status and ret:
                count = 0
                total_count = 0
                for r in ret:
                    for c in r["Contracts"]:
                        total_count += 1
                        if c["Status"] in state:
                            count += 1
                if count == total_count:
                    return True, ret
            used_time = int(time.time()) - start
        return False, ret


if __name__ == "__main__":
    pass
