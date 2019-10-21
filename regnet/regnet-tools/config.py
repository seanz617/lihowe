import os,sys
import json

class config(object):

    config = {
        "env":       "regnet", 
        "overlay":   False, 
        "qos":       True,
        }

    @classmethod
    def dump_config(cls, config_path):
        jsObj = json.dumps(cls.config, indent=4)
        with open(config_path, "w") as f:
            f.write(jsObj)

    @classmethod
    def load_config(cls, config_path):
        with open(config_path, "r") as json_file:
            cls.config = json.loads(json_file.read())

    @classmethod
    def show_config(cls):
        jsObj = json.dumps(cls.config, indent=4)
        logger.info(jsObj, html=True, also_console=True)

    @classmethod
    def switch_overlay(cls, switch):
        pass

    @classmethod
    def switch_qos(cls, switch):
        pass

    @classmethod
    def setup(cls, switch):
        pass

    @classmethod
    def teardown(cls, switch):
        pass

    @classmethod
    def get_miner_name(cls, miner_id):
       return cls.miner.get(miner_id, None) 
    
if __name__ == "__main__":
    config.load_config("./env.conf")
    print config.config
    config_dir = "/home/nfs/regnet-config/master"
    for base,subdirs,files in os.walk(config_dir):
        for file in files:
	    try:
	    	path = os.path.join(base,file)
		context = "" 
		conf = None
            	with open(path, "r") as json_file:
            		context = json_file.read()
            		conf = json.loads(context)
			service_conf = conf.get("Service",None)
			qos_conf = conf.get("QoSServerConfig",None)
			if qos_conf != None:
				conf["QoSServerConfig"]["Enable"] = config.config["qos"]
			elif service_conf != None:
				qos_conf = service_conf.get("QoSServerConfig",None)
				if qos_conf !+ None:
					conf["Service"]["QoSServerConfig"]["Enable"] = config.config["qos"]

			overlay_conf = conf.get("OverlayConfig",None)
			if overlay_conf != None:
				conf["OverlayConfig"]["Switch"] = config.config["overlay"]

		if conf != None:
			jsObj = json.dumps(conf, indent=4)
        		with open(path, "w") as f:
            			f.write(jsObj)
	    except Exception as err:
		print err
		continue
