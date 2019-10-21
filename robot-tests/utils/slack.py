import os
import time
import re
from slackclient import SlackClient


office_result = True
regnet_result = True

#xoxb-386991973601-529617492947-EzE51f5syQYRIAhiVeayqjyl
slack_client = SlackClient("xoxb-386991973601-529617492947-EzE51f5syQYRIAhiVeayqjyl")

'''
#get users
api_call_ret = slack_client.api_call("users.list")
if api_call_ret.get("ok"):
    users = api_call_ret.get("members")
    for user in users:
        if user['name'] == 'tangsan':
            print(user)
'''

slack.chat.post_message('@to_user',msg,username='@from_user')

'''
#message context
context = {
  "text": "Automation Test Report",
  "channel": "chunk_refactoring",
  "attachments": [
    {
      "fallback": "test report",
      "actions": [
        {
          "type": "button",
          "text": "Office",
          "url": "http://192.168.50.220:8080/job/single-go-ppio/HTML_20Report/",
          "style": "primary" if office_result == True else "danger"
        },
        {
          "type": "button",
          "text": "Regent",
          "url": "http://192.168.50.206:8080/job/regnet-test/HTML_20Report/",
          "style": "primary" if regnet_result == True else "danger"
        }
      ]
    }
  ]
}

#send message
slack_client.api_call('chat.postMessage', channel=context["channel"],text=context["text"],attachments=context["attachments"])

#send image
with open("../report/report.png", 'rb') as file_content:
        slack_client.api_call(
                "files.upload",
                channels="chunk_refactoring",
                file=file_content,
                title="test result"
            )
'''
