#pcdn discord wechat消息转发

## 功能点
  - 文本消息转发
  - 图片消息转发
  - 动态添加discord(channel)和wechat(chatroom)转发关系

## 部署
  - 文件列表
    - discord_bot.py
    - wechat_bot.py
    - check_discord_bot.py
    - check_wechat_bot.py
    - config.json
  - 环境
    - PYTHON3环境

    ```bash
    sudo yum install epel-release -y
    sudo yum install https://centos7.iuscommunity.org/ius-release.rpm -y
    sudo yum install python36u -y
    sudo yum install python36u-devel -y
    sudo ln -s /usr/bin/python3.6 /bin/python3

    sudo yum install python36u-pip -y
    sudo ln -s /bin/pip3.6 /bin/pip3

    sudo pip3 install pymysql
    sudo pip3 install itchat
    sudo python3 -m pip install -U discord.py
    ```

    - Mysql环境

    ```bash
    create database message_transfer;
    use message_transfer;
    create table discord_msg(id int auto_increment primary key, type int default 1, author varchar(64) default null, message varchar(512) default null, dests varchar(256) default null, status int default 0, time datetime);
    create table wechat_msg(id int auto_increment primary key, type int default 1, author varchar(64) default null, message varchar(512) default null, dests varchar(256) default null, status int default 0, time datetime);
    ```

    - 部署

      - 添加机器人到DISCORD  
      [具体步骤请参考](https://www.techworm.net/2018/09/how-to-add-bots-to-discord-server.html)
      ```bash
      1.创建DISCORD SERVER
      2.创建DISCORD机器人
      3.获取机器人TOKEN
      4.获取机器人OAuth认证URL，访问URL地址将机器人添加到SERVER中
      5.修改配置文件config.json添加机器人TOKEN
      "discord": {
        "token": "机器人TOKEN",
        "channels": [
            "test-test"
        ]
      },
      ```

      - 部署代码
      ```bash
      cd ~
      mkdir message_transfer
      cp *_bot.py message_transfer/
      cp *_bot.sh message_transfer/
      cd message_transfer
      mkdir images #存放图片文件
      将check_discord_bot.sh加到定时任务里面
      将check_wechat_bot.sh加到定时任务里面
      注：初次启动wechat_bot.py或check_wechat_bot.sh需要手机端扫码登录
      ```

## 建立消息转发通道
  - 方法一 修改配置文件
    - 修改config.json文件，例如添加 test_discord_channel 到 test_wechat_chatroom的消息转发

    ```bash
    "discord": {
        "token": "BOT TOKEN",
        "channels": [
            "test_discord_channel"
        ]
    },
    "wechat": {
        "chatrooms": [
            "test_wechat_chatroom"
        ]
    },
    "message_mapping": {
        "discord": {
            "test_discord_channel": [
                "test_wechat_chatroom"
            ]
        },
        "wechat": {
            "test_wechat_chatroom": [
                "test_discord_channel"
            ]
        }
    }
    ```

  - 方法二 在DISCORD中发送消息
    - 在需要和微信建立转发消息的CHANNEL中发送特定消息，例如

    ```bash
    建立消息转发
    #connect to wechat test_wechat_chatroom
    取消消息转发
    #disconnect to wechat test_wechat_chatroom
    ```
