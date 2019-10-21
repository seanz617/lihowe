import os,sys
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
import json
import uuid
import pymysql

class DB(object):

    def __init__(self, config):
        self.config = config

    def handle(self, cmd, arg=()):
        ret = None 
        db = None
        try:
            db = pymysql.connect(self.config["host"], self.config["user"], self.config["password"], self.config["db"])
            cursor = db.cursor()
            cursor.execute(cmd,arg)
            db.commit()
            ret = cursor.fetchall()
        except Exception as err:
            print(err)
            ret = None
            if db:
                db.rollback()
        finally:
            if db:
                db.close()
        return ret

class User(UserMixin):
    pass
