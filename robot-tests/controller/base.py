import os
import time
import json
import traceback
from robot.api import logger
from test_config import test_config

class base(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, name="test"):
        self.tag = "{}: ".format(name)

    @classmethod
    def parse_param(cls, param):
        ret = param
        if type(param) == str and param[-1] == "]":
            try:
                i = param.rfind("[")
                ret = json.loads(param[0:i].replace("\'","\"")).get(param[i+1:-1], dict({}))
            except Exception as err:
                ret = param

        if "result" in ret.keys():
            ret["result"] = False if ret["result"] == "False" else True
        if "sync" in ret.keys():
            ret["sync"] = False if ret["sync"] == "False" else True
        if "isdir" in ret.keys():
            ret["isdir"] = False if ret["isdir"] == "False" else True
        return ret 

    @classmethod
    def get_time_limit(cls, op, chunks=0, copies=0):
        if chunks != 0:
            os.environ["chunks"] = str(chunks)
        elif chunks == 0:
            chunks = int(os.environ["chunks"]) if os.environ["chunks"].isdigit() else 0

        if copies != 0:
            os.environ["copies"] = str(copies)
        elif copies == 0:
            copies = int(os.environ["copies"]) if os.environ["copies"].isdigit() else 0

        ret = 180
        try:
            conf = test_config.get_config("operation_time_limit")
            ret = conf.get(op, None)[chunks][copies]
        except Exception as err:
            ret = 180
        finally:
            return ret

    def handle(self, target_type, target_name, func_str, timeout=300):
        #  wrapper kube operations
        def worker(*args, **kwargs):
            ret = None
            status = False
            used_time = 0
            try:
                obj = target_type(target_name)
                if hasattr(obj, func_str) == True:
                    func = getattr(obj, func_str)
                    start_time = int(time.time())
                    status,ret = func(*args, **kwargs)
                    used_time = int(time.time()) - start_time
            except Exception as err:
                logger.info("Object: %s, name:%s, func: %s, err info: %s" % (self.tag, target_name, func_str, err),
                            html=True,
                            also_console=True)
                msg = traceback.format_exc()
                logger.info("Track back info: %s" % msg, html=True, also_console=True)
            finally:
                if used_time >= timeout:
                    logger.info("run timeout", html=True, also_console=True)
                return status if used_time <= timeout else False, ret
        return worker

if __name__ == "__main__":
    pass
