import os,sys
import threading
import json

class service_config(object):

    mysql = {
            "host":      "127.0.0.1",
            "port":      3306,
            "user":      "root",
            "password":  "123456",
            "db":        "TestCaseManager"
            }

    config = {
            "mysql":mysql,
        }

    _instance_lock = threading.Lock()

    def __init__(self, config_path = ""):
        if(config_path != ""):
            service_config.load_config(config_path)
        else:
            service_config.load_config("config.json")

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(service_config, "_instance"):
            with service_config._instance_lock:
                if not hasattr(service_config, "_instance"):
                    service_config._instance = super(service_config, cls).__new__(cls) 
        return service_config._instance

    @classmethod
    def dump_config(cls, config_path="config.json"):
        jsObj = json.dumps(cls.config, indent=4)
        with open(config_path, "w") as f:
            f.write(jsObj)

    @classmethod
    def load_config(cls, config_path):
        with open(config_path, "r") as json_file:
            cls.config = json.loads(json_file.read())
            cls.mysql = cls.config["mysql"]

    @classmethod
    def show_config(cls):
        jsObj = json.dumps(cls.config, indent=4)
        print(jsObj)

if __name__ == "__main__":
    pass
