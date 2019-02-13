from nonebot import on_command, CommandSession


__plugin_name__ = "转告"
__plugin_usage__ = """
------retelling------
命令关键字："转告", "通知"
命令输入格式：

转告 <@转告目标> <需告知内容>

效果： 被屏蔽了没关系，我来帮你发过去

########################
"""


@on_command('retelling', aliases=("转告", "通知"), only_to_me=False)
async def retelling(session: CommandSession):
    try:
        into = session.ctx["message"][1]["data"]["qq"]
        info = session.ctx["message"][2]["data"]["text"]
    except IndexError:
        await session.send("转告登记失败")
    else:
        await session.send("[CQ:at,qq={}]{}".format(into, info))