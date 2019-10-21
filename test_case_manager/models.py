import os,sys,json
import pymysql

class DB(object):

    def __init__(self, config):
        self.config = config

    def handle(self, cmd, arg=()):
        ret = None
        status = True
        try:
            db = pymysql.connect(self.config["host"], self.config["user"], self.config["password"], self.config["db"])
            cursor = db.cursor()
            cursor.execute(cmd,arg)
            db.commit()
            ret = cursor.fetchall()
        except Exception as err:
            print("error",cmd)
            print(err)
            ret = str(err)
            status = False
            db.rollback()
        finally:
            db.close()
        return ret, status