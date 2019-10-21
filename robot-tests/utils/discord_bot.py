import sys
import discord
import shlex
import subprocess
import re
from discord.ext import commands

#print(discord.__version__)

user_id_map = {"caiyesd": "",
               "datafingertips": "",
               "tycholiu": "",
               "cestlavie": "",
               "hindsights": "",
               "aldo-lzy": "",
               "cardinalinux": "",
               "huangyuan0pplabs": "",
               "hvmiao": "",
               "liuhongweitet": "",
               "byqgithub": "",
               "tatcimi": ""}

description = 'I\'m a tester'

channel_id = '555317913788219395'
test_channel = discord.Object(id=channel_id)

bot = commands.Bot(command_prefix='#', description=description)

test_report_msg = '@everyone'

test_branch = sys.argv[1]
test_result = sys.argv[2].split(" ")

def get_commit_info():
    output = ""
    command = shlex.split("git log --pretty=format:\"%h - %an, %ar : %s\" -n 1")
    try:
        output = subprocess.check_output(command, shell=False, timeout=10, stderr=subprocess.STDOUT, cwd="/home/workspace/go/src/github.com/PPIO/go-ppio").decode()
    except Exception as err:
        output = ""
        print(err)
    commit_info = [ i.strip() for i in re.split('[-,:]', str(output))]
    return commit_info

@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)

    commit_info = get_commit_info()
    print(commit_info)

    server = None
    for s in bot.servers:
        if s.name == "TestServer":
            server = s
            break

    if server != None:
        #for m in server.members:
        #    print(m.name, m.id)

        embed = discord.Embed(title="Daily Test Report", type="rich", color=0x00FF00, url="http://192.168.50.206:8080/view/daily_build/job/daily_auto_test_for_{}/HTML_20Report/".format(test_branch))
        #embed.set_image(url = "")
        embed.add_field(name="Branch", value=test_branch, inline=True)
        embed.add_field(name="Commit ID", value=commit_info[0], inline=True)
        embed.add_field(name="Commit info", value=commit_info[3], inline=False)
        embed.add_field(name="Total", value=test_result[2], inline=True)
        embed.add_field(name="Pass", value=test_result[0], inline=True)
        embed.add_field(name="Fail", value=test_result[1], inline=True)
        embed.add_field(name="Log", value="http://192.168.50.206:8080/view/daily_build/job/daily_auto_test_for_{}/ws/".format(test_branch), inline=True)
        #embed.set_footer(text='', icon_url="")

        try:
            await bot.send_message(test_channel, test_report_msg, embed=embed)
            #await bot.send_file(test_channel, 'report.png')
        except Exception as err:
            print(err)
        finally:
            await bot.logout()

@bot.event
async def on_message(message):
    if message.content.startswith('greet'):
        await bot.send_message(message.channel, 'Say hello')
        msg = await bot.wait_for_message(author=message.author, content='hello')
        msg_ = 'Hello {0.author.mention}'.format(msg)
        #bot.get_all_channels():
        #bot.servers:
        #message.server.members:
        await bot.send_message(message.channel, "Hello <@554580702218289153>")

if __name__ == "__main__":
    bot.run('NTU1MDE2NzAxOTcyOTcxNTMw.D2pXOg.BahvMt2c2LLwEw6C8qB1v6mDKKs')
