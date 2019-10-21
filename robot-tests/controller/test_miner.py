import os,sys,time,datetime
from robot.api import logger
from indexer import indexer
from miner import miner
from poss import poss
from base import base
from test_config import test_config

class test_miner(base):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        base.__init__(self, self.__class__.__name__)
    '''
    def extend_miner_storage(self, miner_no, indexer_no):
        miner_obj = miner(miner_no)

        #get origin storage info
        status, ret = self.handle(indexer, indexer_no, "available_miners")()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        old_indexer_storage_info = ret

        status, ret = miner_obj.get_plot_size()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        old_plot_size = int(ret)

        status, ret = miner_obj.storage_info()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        old_storage_info = ret
    
        #set storage info
        status, ret = miner_obj.set_plot_size(old_plot_size * 2)
        if status == False:
            logger.info("",html=True,also_console=True)
            return False

        status, ret = miner_obj.adjust_plot_count(old_storage_info["TotalPlotCount"] + 1)
        if status == False:
            logger.info("",html=True,also_console=True)
            return False

        time.sleep(120)

        #get new storage info
        status, ret = miner_obj.get_plot_size()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        new_plot_size = int(ret)

        status, ret = miner_obj.storage_info()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        new_storage_info = ret
         
        status, ret = self.handle(indexer, indexer_no, "available_miners")()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        new_index_storage_info = ret
       
        #check miner storage info
        if (old_plot_size * 2) != new_plot_size:
            logger.info("plot size error",html=True,also_console=True)
            return False

        if new_storage_info["TotalPlotCount"] != (old_storage_info["TotalPlotCount"] + 1):
            logger.info("total plot count error",html=True,also_console=True)
            return False
      
        mc = test_config.get_config(miner_no)
        mi = None
        for m in new_index_storage_info:
            if m["MinerID"] == mc["account"]:
                mi = m
                break
        if mi == None or int(new_storage_info["TotalPlotSize"]) != int(mi["TotalSpace"]):
            logger.info("total space error",html=True,also_console=True)
            return False

    def shrink_miner_storage(self, miner_no, indexer_no):
        miner_obj = miner(miner_no)

        #get origin storage info
        status, ret = self.handle(indexer, indexer_no, "available_miners")()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        old_indexer_storage_info = ret

        status, ret = miner_obj.get_plot_size()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        old_plot_size = int(ret)

        status, ret = miner_obj.storage_info()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        old_storage_info = ret
       
        #set storage info
        status, ret = miner_obj.set_plot_size(old_plot_size / 2)
        if status == False:
            logger.info("",html=True,also_console=True)
            return False

        status, ret = miner_obj.adjust_plot_count(old_storage_info["TotalPlotCount"] - 1)
        if status == False:
            logger.info("",html=True,also_console=True)
            return False

        time.sleep(120)

        #get new storage info
        status, ret = miner_obj.get_plot_size()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        new_plot_size = int(ret)

        status, ret = miner_obj.storage_info()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        new_storage_info = ret
         
        status, ret = self.handle(indexer, indexer_no, "available_miners")()
        if status == False:
            logger.info("",html=True,also_console=True)
            return False
        new_index_storage_info = ret
       
        #check miner storage info
        if (old_plot_size / 2) != new_plot_size:
            logger.info("plot size error",html=True,also_console=True)
            return False

        if new_storage_info["TotalPlotCount"] != (old_storage_info["TotalPlotCount"] - 1):
            logger.info("total plot count error",html=True,also_console=True)
            return False
      
        mc = test_config.get_config(miner_no)
        mi = None
        for m in new_index_storage_info:
            if m["MinerID"] == mc["account"]:
                mi = m
                break
        if mi == None or int(new_storage_info["TotalPlotSize"]) != int(mi["TotalSpace"]):
            logger.info("total space error",html=True,also_console=True)
            return False
    '''
    def miner_will_leave(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","miner0")
        expect = dict_param.get("result", True)
        leave_time = dict_param.get("leave_time", 30)

        assert expect == self.handle(miner, operator, "will_leave")(leave_time)[0]

    def stop_miner(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","miner0")
        expect = dict_param.get("result", True)

        assert expect == self.handle(miner, operator, "stop_daemon")()[0]

    def clear_miner(self, dict_param):
        dict_param = self.parse_param(dict_param)
        operator = dict_param.get("node","miner0")
        expect = dict_param.get("result", True)
        
        assert expect == self.handle(miner, operator, "chunk_clear")()[0]

        if expect:
            time.sleep(30)
            status, ret = self.handle(miner, operator, "chunk_list")() 
            assert not (ret != None or not status)

if __name__ == "__main__":
    pass
