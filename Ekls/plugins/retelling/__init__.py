from nonebot import on_command, CommandSession

@on_command('retelling', aliases=("转告", "通知"), only_to_me=False)
async def retelling(session: CommandSession):
    try:
        into = session.ctx["message"][1]["data"]["qq"]
        info = session.ctx["message"][2]["data"]["text"]
    except KeyError:
        await session.send("转告登记失败")
    else:
        await session.send("[CQ:at,qq={}]，[CQ:at,qq={}]让我转告你:'{}'".format(into, session.ctx["user_id"], info))