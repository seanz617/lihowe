import os,sys,time,threading,json
import pymysql
import discord
import asyncio
from discord.ext import commands
from discord import File

def load_config(config_path):
    with open(config_path, "r") as json_file:
        return json.loads(json_file.read())

config = load_config("./config.json")

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
        status = False
        ret = None
        db.rollback()
    finally:
        db.close()
        return status, ret

run_flag = True

pic_ext = ["png","jpg","jpeg"]

discord_token = config["discord"]["token"]

client = discord.Client()

async def transfer_msg_task():
    await client.wait_until_ready()
    while run_flag and not client.is_closed():
        status, messages = handle_sql("select * from wechat_msg where status=0;")
        if status and messages:
            for m in messages:
                message_type = int(m[1])
                if message_type != 1 and message_type != 2:
                    continue

                dests = m[4].split(",")
                channel_objs = []
                channel_list = client.get_all_channels()
                channel_dict = dict({})
                for c in channel_list:
                    channel_dict[c.name] = c.id
                print(channel_dict)
                for d in dests:
                    if d in channel_dict:
                        channel_objs.append(client.get_channel(channel_dict[d]))
                if len(channel_objs) <= 0:
                    continue

                msg = m[3].replace("?", "")
                if msg != '':
                    if message_type == 1:
                        msg = "[{}]:{}".format(m[2],msg)
                        for c in channel_objs:
                            print("send message to discord ",msg)
                            await c.send(msg)
                        handle_sql("update wechat_msg set status=1 where id={}".format(m[0]))

                    elif message_type == 2:
                        msg_title = "[picture from:{}]".format(m[2])
                        file_size = os.path.getsize("./images/{}".format(msg))
                        send_image = True
                        if file_size >= 1048576:
                            send_image = False
                            msg_title += " image too big can't send to discord"
                        for c in channel_objs:
                            print("send message to discord ", msg_title)
                            await c.send(msg_title)
                            if send_image: 
                                print("send image to discord ", msg)
                                await c.send(file=File("./images/{}".format(msg)))
                        handle_sql("update wechat_msg set status=1 where id={}".format(m[0]))
        await asyncio.sleep(1)

@client.event
async def on_ready():
    print("login discord as ",client.user.name)

@client.event
async def on_message(message):
    message_type = 1
    config = load_config("./config.json")
    if message.content.startswith("#connect to wechat "):
        chatroom_name = message.content[19:]
        if not message.channel.name in config["discord"]["channels"]:
            config["discord"]["channels"].append(message.channel.name)
        if not chatroom_name in config["wechat"]["chatrooms"]:
            config["wechat"]["chatrooms"].append(chatroom_name)

        if not message.channel.name in config["message_mapping"]["discord"].keys():
            config["message_mapping"]["discord"][message.channel.name] = [chatroom_name]
        elif not chatroom_name in config["message_mapping"]["discord"][message.channel.name]:
            config["message_mapping"]["discord"][message.channel.name].append(chatroom_name)

        if not chatroom_name in config["message_mapping"]["wechat"].keys():
            config["message_mapping"]["wechat"][chatroom_name] = [message.channel.name]
        elif not message.channel.name in config["message_mapping"]["wechat"][chatroom_name]:
            config["message_mapping"]["wechat"][chatroom_name].append(message.channel.name)

        jsObj = json.dumps(config, indent=4)
        with open("config.json", "w") as f:
            f.write(jsObj)
        return

    if message.content.startswith("#disconnect to wechat "):
        chatroom_name = message.content[22:]

        if message.channel.name in config["message_mapping"]["discord"].keys():
            config["message_mapping"]["discord"][message.channel.name].remove(chatroom_name)
        if chatroom_name in config["message_mapping"]["wechat"].keys():
            config["message_mapping"]["wechat"][chatroom_name].remove(message.channel.name)

        jsObj = json.dumps(config, indent=4)
        with open("config.json", "w") as f:
            f.write(jsObj)

        return

    if message.channel.name in config["discord"]["channels"] and message.author != client.user:
        author_name = "{} {}".format(message.channel.name, message.author.name)
        image_files = []
        if message.attachments:
            for att in message.attachments:
                url = att.url.lower()
                for ext in pic_ext:
                    if url.endswith(ext):
                        message_type = 2
                        os.system("wget -P {} {}".format("./images", att.url))
                        image_files.append(att.filename)
        print("receive discord message ", message.author.name, message.content, image_files, message_type)

        dests = config["message_mapping"]["discord"].get(message.channel.name,"")
        if dests and len(dests) > 0:
            dests_str = ",".join(dests)
            msg = ",".join(image_files) if message_type == 2 else message.content
            print(msg)
            handle_sql("insert into discord_msg(type,author,message,dests,time) values({},\'{}\',\'{}\',\'{}\',NOW());".format(message_type, author_name, msg, dests_str))

client.loop.create_task(transfer_msg_task())
client.run(discord_token)
