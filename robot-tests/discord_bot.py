import os,sys,time,threading,json
import shlex
import subprocess
import re
import discord
import asyncio
from discord.ext import commands

client = discord.Client()
channel_id = '555317913788219395'

test_report_msg = '@everyone'

test_branch = sys.argv[1]
test_commit_id = sys.argv[2]
test_report_title = sys.argv[3]
test_result = sys.argv[4].split(" ")

@client.event
async def on_ready():
    channel_list = client.get_all_channels()
    for c in channel_list:
        if c.name == "test-report":
            target_channel = c
            break
    if target_channel:
        embed = discord.Embed(title=test_report_title, type="rich", color=0x00FF00, url="http://192.168.50.206:8080/job/submit_build_for_{}/HTML_20Report/".format(test_branch))
        embed.add_field(name="Branch", value=test_branch, inline=True)
        embed.add_field(name="Commit ID", value=test_commit_id, inline=True)
        embed.add_field(name="Total", value=test_result[2], inline=True)
        embed.add_field(name="Fail", value=test_result[1], inline=True)
        embed.add_field(name="Log", value="http://192.168.50.206:8080/view/daily_build/job/daily_auto_test_for_{}/ws/".format(test_branch), inline=True)

        try:
            await target_channel.send(test_report_msg, embed=embed)
        except Exception as err:
            print(err)
        finally:
            await client.logout()

if __name__ == "__main__":
    client.run('NTU1MDE2NzAxOTcyOTcxNTMw.D2pXOg.BahvMt2c2LLwEw6C8qB1v6mDKKs')
