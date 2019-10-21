import os
import sys
import json
from robot.api import logger

from db import db
from rpc import rpc
from proc import proc
from test_config import test_config
from factory import ManagerFactory


class node(object):

    def __init__(self, name):
        # node environment(tuple)
        self.name = name
        self.env = test_config.get_config("env")
        self.subenv = test_config.get_config("subenv")
        self.parallel = test_config.get_config("parallel")
        self.node_config = test_config.get_config(name)
        self.request_id = 1

        # general tools
        self.default = test_config.get_config("default")
        self.db_handler = db(test_config.get_config("mysql"))
        self.rpc_handler = rpc(test_config.get_config("rpc"))
        self.proc_handler = proc()
        self.process_manager = ManagerFactory().create_manager(test_config)
        # self.kube_handler = None
        # if "R" in self.env:
        #     kube_config = os.path.join(os.path.dirname(os.environ.get("TEST_CONFIG", "")),
        #                                test_config.kube.get("kube_config", ""))
        #     resource_config = os.path.join(os.path.dirname(os.environ.get("TEST_CONFIG", "")),
        #                                    test_config.kube.get("resource_config", ""))
        #     if not os.path.exists(kube_config):
        #         kube_config = os.path.join(os.path.dirname(__file__),
        #                                    "..",
        #                                    "config",
        #                                    test_config.kube.get("kube_config", ""))
        #         resource_config = os.path.join(os.path.dirname(__file__),
        #                                        "..",
        #                                        "config",
        #                                        test_config.kube.get("resource_config", ""))
        #     if os.path.exists(kube_config):
        #         self.kube_handler = Kube(kube_config, resource_config)

    def handle(self, *args, **kargs):
        ret = {}
        tag = "{}:{}:{} || ".format(self.name, sys._getframe().f_back.f_code.co_name, locals())
        command = kargs["command"]
        params = kargs["params"]

        # get node ip and rpc service port
        ip = self.node_config["ip"]
        port = self.node_config["port"] 

        # send http post request
        if ip is not None and port is not None:
            ret = self.rpc_handler.handle(ip, port, command, params, self.request_id)
            if ret is None:
                return False, None
            self.request_id += 1
            ret = ret.replace("\n", "")
            ret = ret.replace("\\n", "")
            ret = json.loads(ret)
            if "result" in ret.keys() and \
                    type(ret["result"]) == dict and \
                    "ExResult" in ret["result"].keys() and \
                    type(ret["result"]["ExResult"]) == str:
                tmp_str = ret["result"]["ExResult"]
                try:
                    ret["result"]["ExResult"] = json.loads(ret["result"]["ExResult"])
                except Exception as err:
                    ret["result"]["ExResult"] = tmp_str
            elif "result" in ret.keys() and type(ret["result"]) == str:
                tmp_str = str()
                try:
                    tmp_str = ret["result"]
                    ret["result"] = json.loads(ret["result"])
                except Exception as err:
                    ret["result"] = tmp_str
            elif "error" in ret.keys() and isinstance(ret.get("error", ""), dict):
                ret["error"] = ret.get("error", "")
        else:
            logger.info(tag + "get node ip:port error", html=True, also_console=True)

        logger.info(tag + str(ret), html=True, also_console=True)

        if "result" in ret.keys():
            return True, ret["result"]
        return False, ret.get("error", str(ret))

    # def launch_node(self):
    #     ret = None
    #     tag = "{}:{}:{} || ".format(self.name, sys._getframe().f_back.f_code.co_name, locals())
    #     logger.info("launch node " + self.name, html=True, also_console=True)
    #
    #     if(self.environment[0] == "R"):
    #         ret = self.kube_handler.create_resource(self.node_config)
    #     elif(self.environment[0] == "S"):
    #         ret = self.proc_handler.create_proc(self.node_config)
    #
    #     if ret == None:
    #         logger.info(tag + "node start error",html=True,also_console=True)
    #     return ret
    #
    # def destroy_node(self):
    #     ret = None
    #     logger.info("delete node " + self.name, html=True, also_console=True)
    #
    #     if(self.environment[0] == "R"):
    #         ret = self.kube_handler.delete_resource(self.node_config)
    #     elif(self.environment[0] == "S"):
    #         ret = self.proc_handler.delete_proc(self.node_config)
    #
    #     return ret


if __name__ == "__main__":
    print(os.path.join(os.path.dirname(__file__), "..", "config"))
    pass
