import multiprocessing
import subprocess
import signal
import time
import datetime
from robot.api import logger

class proc(object):

    def __init__(self):
        pass

    def create_proc(self, config):
        proc = None

        try:
            with open(config["log_path"],"w") as loghandle:
                proc = subprocess.Popen([config["command"], config["subcommand"], "--datadir="+config["config_path"]], cwd=".", shell=False, stdout=loghandle, stderr=loghandle)
        except Exception as err:
            logger.info(err, html=True, also_console=True)

        return proc

    def delete_proc(self, name):
        ret = None
        if self.procs.get(name) != None:
            self.procs[name]["proc"].send_signal(signal.SIGINT)
            #self.procs[name]["proc"].send_signal(signal.CTRL_C_EVENT)
            #self.procs[name]["proc"].kill()
            #self.procs[name]["proc"].terminate()
        return ret

if __name__ == "__main__":
    obj = proc()
    c = {
            "config_path":"/home/workspace/tmp/regnet-config/master/user0",
            "log_path":"./poss0.log",
            "command":"/home/workspace/go/src/github.com/PPIO/go-ppio/cmd/poss/poss",
            "subcommand":"start",
            }
    obj.create_proc(c)
