import os,sys,time
from robot.api import logger
from node import node
from db import db

class indexer(node):

    def __init__(self, name):
        node.__init__(self, name)

    def truncate_table(self, table_name):
        return self.db_handler.handle(["truncate table {}".format(table_name)])

    def peer_available(self, peerid):
        pass

    def query_account(self, params):
        pass

    def available_miners(self):
        return self.handle(command="AllValidMiner",params=[])

if __name__ == "__main__":
    pass
