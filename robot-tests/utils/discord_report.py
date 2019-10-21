import os
import sys
import discord


client = discord.Client()
channel_id = 593016617961783296

test_report_msg = ''

test_branch = sys.argv[1]
test_commit_id = sys.argv[2]
test_result = sys.argv[3].split(" ") if " " in sys.argv[3] else sys.argv[3]
if len(sys.argv) > 4:
    project_name = sys.argv[4]
else:
    project_name = os.environ.get("JOB_NAME", "Can not get project name from jenkins")
job_url = os.environ.get("JOB_URL", "http://192.168.2.206:8080/")
log_url = os.environ.get("BUILD_URL") + "console" if os.environ.get("BUILD_URL", "") else "NULL"
report_path = "artifact/go/src/github.com/PPIO/ppio-tests/cases/automation/robot-tests/result/report.html"
report_url = os.environ.get("BUILD_URL") + report_path if os.environ.get("JOB_URL", "") else "NULL"


@client.event
async def on_ready():
    target_channel = None
    channel_list = client.get_all_channels()
    for c in channel_list:
        if c.id == channel_id:
            target_channel = c
            break
    if target_channel:
        embed = discord.Embed(title=project_name, type="rich", color=0x00FF00, url=job_url)
        embed.add_field(name="Branch", value=test_branch, inline=True)
        embed.add_field(name="Commit ID", value=test_commit_id, inline=True)
        if isinstance(test_result, list):
            embed.add_field(name="Total", value=test_result[2], inline=True)
            embed.add_field(name="Fail", value=test_result[1], inline=True)
            embed.add_field(name="Report", value=report_url, inline=True)
        else:
            embed.add_field(name="Result", value=test_result, inline=True)
            embed.add_field(name="Log", value=log_url, inline=True)

        try:
            await target_channel.send(test_report_msg, embed=embed)
        except Exception as err:
            print(err)
        finally:
            await client.logout()

if __name__ == "__main__":
    client.run('NTU1MDE2NzAxOTcyOTcxNTMw.D2pXOg.BahvMt2c2LLwEw6C8qB1v6mDKKs')
