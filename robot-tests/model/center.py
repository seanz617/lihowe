import os,sys,time
from robot.api import logger
from node import node

class center(node):

    def __init__(self, name):
        node.__init__(self, name)

    def list_server(self):
        status,ret = self.handle(command="ListServers",params=[])
        if(status == True and ret != None):
            if(len(ret["Indexers"]) > 0 and len(ret["Verifiers"]) > 0):
                return True,ret
        return False,ret

if __name__ == "__main__":
    pass
