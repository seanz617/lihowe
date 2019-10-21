import os,sys
from robot.api import logger
from bootstrap import bootstrap
from indexer import indexer
from base import base

class test_indexer(base):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        base.__init__(self,  self.__class__.__name__) 

    def clear_storage_contracts(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("indexer","indexer0")
        expect = dict_param.get("result",True)

        assert expect == self.handle(indexer, operator, "truncate_table")("storage_contract")[0]

if __name__ == "__main__":
    pass
