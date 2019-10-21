import os,sys
import pymysql
from robot.api import logger

class db(object):

    def __init__(self, config):
        self.config = config

    def handle(self, commands):
        status = True
        ret = None 
        try:
            db = pymysql.connect(self.config["host"], self.config["user"], self.config["password"], self.config["db"])
            cursor = db.cursor()
            for cmd in commands:
                cmd = cmd + ";"
                print(cmd)
                cursor.execute(cmd)
                db.commit()
            ret = cursor.fetchall()
        except Exception as err:
            status = False
            ret = None
            logger.info(err,html=True,also_console=True)
            db.rollback()
        finally:
            db.close()
        return status, ret
