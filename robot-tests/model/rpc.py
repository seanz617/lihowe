import os,sys,time
from robot.api import logger
import json
import requests


class rpc(object):

    def __init__(self, config):
        self.headers = config["headers"] 
        self.timeout = config["timeout"] 
        self.internal = config["internal"] 
        self.tag = "rpc: || "

    def worker(self, url, headers, data):
        ret = None
        time.sleep(1)
        retry_times = 1
        for i in range(retry_times):
            try:
                response = requests.post(url, data=data, headers=headers, timeout=self.timeout)

                if response.status_code == 200:
                    ret = response.text
                    break
                time.sleep(self.internal)
            except Exception as err:
                if data.find("StopDaemon") >= 0:
                    ret = '{"result":"Stop Daemon Success"}' 
                    break
                logger.info(self.tag + str(err),html=True,also_console=True)
        return ret

    def handle(self, ip, port, command, params, request_id):
        url = "http://{}:{}/rpc".format(ip,port)
        body = {"jsonrpc":"2.0","method":command,"params":params,"id":request_id}
        return self.worker(url, self.headers, json.dumps(body))


if __name__ == "__main__":
    pass
