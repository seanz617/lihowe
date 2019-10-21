import os,sys,time,threading,json
import pymysql
import itchat
from itchat.content import *

run_flag = True

def load_config(config_path):
    with open(config_path, "r") as json_file:
        return json.loads(json_file.read())

config = load_config("./config.json")

# id type author message dest status time
def handle_sql(command):
    status = True
    ret = None
    try:
        db = pymysql.connect(config["mysql"]["host"], config["mysql"]["user"], config["mysql"]["password"], config["mysql"]["db"])
        cursor = db.cursor()
        cursor.execute(command)
        db.commit()
        ret = cursor.fetchall()
    except Exception as err:
        print(err)
        status = False
        ret = None
        db.rollback()
    finally:
        db.close()
        return status, ret

def exitCallback():
    run_flag = False
    print("LOG OUT! please relogin")
    time.sleep(1)
    os._exit() 

last_msg_id = {"id":""}
@itchat.msg_register([TEXT,PICTURE], isGroupChat=True)
def handler_receive_msg(msg):
    try:
        if msg["MsgId"] == last_msg_id["id"]:
            print("recv same message ", last_msg_id, msg["MsgId"]) 
            return

        last_msg_id["id"] = msg["MsgId"]
        config = load_config("./config.json")
        if msg["User"]["NickName"] in config["wechat"]["chatrooms"]:# and msg["FromUserName"] != msg["User"]["Self"]["UserName"]:
            author_name = "{} {}".format(msg["User"]["NickName"], msg['ActualNickName'])
            dests = config["message_mapping"]["wechat"].get(msg["User"]["NickName"], [])
            if dests and len(dests) > 0:
                dests_str = ",".join(dests)
                if msg["Type"] == TEXT:
                    print("receive text {}".format(msg["Text"]))
                    handle_sql("insert into wechat_msg(type, author, message, dests, time) values(\'{}\',\'{}\',\'{}\',\'{}\',NOW());".format(1, author_name, msg["Text"], dests_str))

                elif msg["Type"] == PICTURE:
                    print("receive picture {}".format(msg["FileName"]))
                    msg.download("./images/{}".format(msg["FileName"]))
                    handle_sql("insert into wechat_msg(type, author, message, dests, time) values(\'{}\',\'{}\',\'{}\',\'{}\',NOW());".format(2, author_name, msg["FileName"], dests_str))
    except Exception as err:
        print("receive wechat message fail",err)

def send_notification():
    while run_flag:
        try:
            status, messages = handle_sql("select * from discord_msg where status=0;")
            if status and messages:
                for m in messages:
                    message_type = int(m[1])
                    if message_type != 1 and message_type != 2:
                        continue

                    dests = m[4].split(",")
                    if len(dests) <= 0:
                        continue

                    msg = m[3].replace("?", "")
                    if msg != '':
                        if message_type == 1:
                            msg = "[{}]:{}".format(m[2],msg)
                            for d in dests:
                                chat_rooms = itchat.search_chatrooms(d)
                                if chat_rooms:
                                    ret = itchat.send(msg=msg, toUserName=chat_rooms[0]["UserName"])
                            handle_sql("update discord_msg set status=1 where id={}".format(m[0]))

                        elif message_type == 2:
                            msg_title = "[picture from:{}]".format(m[2])
                            for d in dests:
                                chat_rooms = itchat.search_chatrooms(d)
                                if chat_rooms:
                                    ret = itchat.send(msg=msg_title, toUserName=chat_rooms[0]["UserName"])
                                    ret = itchat.send_image(fileDir="./images/{}".format(msg), toUserName=chat_rooms[0]["UserName"])
                            handle_sql("update discord_msg set status=1 where id={}".format(m[0]))
            time.sleep(1)
        except Exception as err:
            print("send message to wechat ",err)

itchat.auto_login(hotReload=True, enableCmdQR=2, exitCallback=exitCallback)
#itchat.auto_login(hotReload=True)
itchat.dump_login_status()

try:
    t = threading.Thread(target=send_notification).start()
    while run_flag:
        itchat.auto_login(hotReload=True, enableCmdQR=2)
        itchat.run()
        print("itchat logout now retrying")
        time.sleep(60)
except KeyboardInterrupt:
    run_flag = False
    time.sleep(3)
    os._exit()
except Exception as err:
    run_flag = False
    print("wechat ",err)
    os._exit()
