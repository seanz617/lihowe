import os,sys
from robot.api import logger
from base import base
from bootstrap import bootstrap
from indexer import indexer

class test_env(base):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        base.__init__(self, self.__class__.__name__) 

    def check_env(self, dict_param):
        dict_param = self.parse_param(dict_param)
        bootstrap_operator = dict_param.get("bootstrap","bootstrap0")
        indexer_operator = dict_param.get("indexer","indexer0")
        indexer_num = dict_param.get("indexer_num",1)
        verifier_num = dict_param.get("verifier_num",1)
        miner_num = dict_param.get("miner_num",10)

        status, ret = self.handle(bootstrap, bootstrap_operator, "list_server")()
        assert status and len(ret["Indexers"]) == indexer_num and len(ret["Verifiers"]) == verifier_num

        status, ret = self.handle(indexer, indexer_operator, "available_miners")()
        assert status and len(ret) == miner_num


if __name__ == "__main__":
    pass
