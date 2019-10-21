import os,sys
import threading
import json
import yaml
from robot.api import logger

class test_config(object):
    env = ""
    subenv = ""
    parallel = False
    kube = dict({})
    mysql = dict({})
    redis = dict({})
    rpc = dict({})
    cmd_line = dict({})
    dirs = dict({})
    resource = dict({})
    operation_time_limit = dict({})
    default = dict({})

    config = {
            "env": env,
            "subenv": subenv,
            "parallel": parallel,
            "kube": kube,
            "mysql": mysql,
            "redis": redis,
            "rpc": rpc,
            "cmd_line": cmd_line,
            "dirs": dirs,
            "resource": resource,
            "default": default,
            "operation_time_limit": operation_time_limit
        }

    config_path = os.environ.get("TEST_CONFIG", "")
    assert os.path.exists(config_path)

    env = os.environ.get("TEST_ENV", "")
    assert env == "R" or env == "S"

    subenv = os.environ.get("TEST_SUBENV", "")
    assert len(subenv) > 0, "Can not get test subenv environ"

    with open(config_path, "r") as json_file:
        config = json.loads(json_file.read())
        config["env"] = env
        config["subenv"] = subenv
        parallel = config["parallel"]
        kube = config["kube"]
        mysql = config["mysql"]
        redis = config["redis"]
        rpc = config["rpc"]
        cmd_line = config["cmd_line"]
        dirs = config["dirs"],
        resource = config["resource"]
        default = config["default"]
        operation_time_limit = config["operation_time_limit"]

    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(test_config, "_instance"):
            with test_config._instance_lock:
                if not hasattr(test_config, "_instance"):
                    test_config._instance = super(test_config, cls).__new__(cls) 
        return test_config._instance

    @classmethod
    def dump_config(cls, config_path):
        jsObj = json.dumps(cls.config, indent=4)
        with open(config_path, "w") as f:
            f.write(jsObj)

    @classmethod
    def load_config(cls):
        config_path = os.environ.get("TEST_CONFIG", "")
        if not os.path.exists(config_path):
            logger.info("not found or wrong TEST_CONFIG environment variable", html=True, also_console=True)
            return

        cls.env = os.environ.get("TEST_ENV", "")
        if cls.env == "" or (cls.env != "R" and cls.env != "S"):
            logger.info("not found or wrong TEST_ENV environment variable", html=True, also_console=True)
            return

        cls.subenv = os.environ.get("TEST_SUBENV", "")
        if not cls.subenv:
            logger.info("Can not get test subenv environ", html=True, also_console=True)
            return

        with open(config_path, "r") as json_file:
            cls.config = json.loads(json_file.read())
            cls.subenv = cls.config["subenv"]
            cls.parallel = cls.config["parallel"]
            cls.kube = cls.config["kube"]
            cls.mysql = cls.config["mysql"]
            cls.redis = cls.config["redis"]
            cls.rpc = cls.config["rpc"]
            cls.cmd_line = cls.config["cmd_line"]
            cls.dirs = cls.config["dirs"]
            cls.resource = cls.config["resource"]
            cls.default = cls.config["default"]
            cls.operation_time_limit = cls.config["operation_time_limit"]

    @classmethod
    def show_config(cls):
        jsObj = json.dumps(cls.config, indent=4)
        logger.info(jsObj, html=True, also_console=True)

    @classmethod
    def get_node_config(cls, name):
        if(cls.env in cls.resource.keys() 
                and cls.subenv in cls.resource[cls.env].keys()
                and name in cls.resource[cls.env][cls.subenv].keys()):
            return cls.resource[cls.env][cls.subenv][name]
        return None 

    @classmethod
    def get_config(cls, name):
        ret = None
        try:
            ret = cls.config[name][cls.env][cls.subenv]
        except Exception as err:
            ret = None
        if ret == None:
            try:
                ret = cls.config[name][cls.env]
            except Exception as err:
                ret = None
        if ret == None:
            try:
                ret = cls.config[name]
            except Exception as err:
                ret = None

        if ret == None:
            for k in cls.config.keys():
                try:
                    ret = cls.config[k][name]
                except Exception as err:
                    ret = None
                if ret == None:
                    try:
                        ret = cls.config[k][cls.env][name]
                    except Exception as err:
                        ret = None
                    if ret == None:
                        try:
                            ret = cls.config[k][cls.env][cls.subenv][name]
                        except Exception as err:
                            ret = None
                if ret != None:
                    break
        return ret

    @classmethod
    def get_nodes(cls):
        if(cls.env in cls.resource.keys() 
                and cls.subenv in cls.resource[cls.env].keys()):
            return cls.resource[cls.env][cls.subenv]
        return None 

    @classmethod
    def get_env(cls):
        return cls.env

    @classmethod
    def get_subenv(cls):
        return cls.subenv

    @classmethod
    def get_mysql(cls):
        if(cls.env in cls.mysql.keys() 
                and cls.subenv in cls.mysql[cls.env].keys()):
            return cls.mysql[cls.env][cls.subenv]
        return None 

    @classmethod
    def get_miner_by_id(cls, miner_id):
        for m in cls.config["resource"][cls.env][cls.subenv].keys():
            if m.find("miner") >= 0 and cls.config["resource"][cls.env][cls.subenv][m]["account"] == miner_id:
                return m, cls.config["resource"][cls.env][cls.subenv][m]
        return ""


if __name__ == "__main__":
    print("config: %s" % test_config.kube.get("kube_config", ""))
    pass
