import os,sys,time
from robot.api import logger
import json
from node import node

class miner(node):

    def __init__(self, name):
        node.__init__(self, name)

    #---------used frequently functions-----------
    def contract_info(self):
        return self.handle(command="ContractInfo",params=[])

    def chunk_list(self):
        return self.handle(command="ChunkList",params=[])

    def chunk_info(self, chunk_hash):
        params = [chunk_hash]
        return self.handle(command="ChunkInfo",params=[chunk_hash])

    def chunk_delete(self, chunk_hash):
        params = [chunk_hash]
        return self.handle(command="ChunkDelete",params=[chunk_hash])

    def chunk_clear(self):
        return self.handle(command="ChunkClear",params=[])

    #------------used rarely functions-----------
    def chunk_export(self,params):
        return self.handle(command="ChunkExport",params=params)

    def chunk_piece(self, params):
        return self.handle(command="ChunkPiece",params=params)

    def chunk_hot_requested(self, params):
        return self.handle(command="ChunkHotRequest",params=params)

    def chunk_hot_downloaded(self, params):
        return self.handle(command="ChunkHotDownload",params=params)

    def chunk_info_with_contract(self, params):
        return self.handle(command="ChunkInfoWithContract",params=params)

    def chunk_list_with_contract(self):
        return self.handle(command="ChunkListWithContract",params=[])

    def net_status(self, params):
        return self.handle(command="NetStatus",params=params)

    def contract_update(self, params):
        return self.handle(command="ContractUpdate",params=[bucket_name])

    def will_leave(self, leave_time):
        return self.handle(command="WillLeave",params=[leave_time])

    def set_plot_size(self, plot_size):
        return self.handle(command="SetPlotSize",params=[plot_size])

    def get_plot_size(self):
        return self.handle(command="GetPlotSize",params=[])

    def adjust_plot_count(self, plot_count):
        return self.handle(command="AdjustPlotCount",params=[plot_count])

    def storage_info(self):
        return self.handle(command="StorageInfo",params=[])

    def stop_daemon(self):
        return self.handle(command="StopDaemon",params=[])

if __name__ == "__main__":
    pass
if __name__ == "__main__":
    pass
