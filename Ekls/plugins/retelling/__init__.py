from nonebot import on_command, CommandSession, get_bot
from nonebot.permission import SUPERUSER


__plugin_name__ = "转告"
__plugin_usage__ = """
------retelling------
命令关键字："转告", "通知"
命令输入格式：

转告 <@转告目标> <需告知内容>

效果： 被屏蔽了没关系，我来帮你发过去

########################

$ 另外放了一些内部管理命令
"""


@on_command('retelling', aliases=("转告", "通知"), only_to_me=False)
async def retelling(session: CommandSession):
    try:
        into = session.ctx["message"][1]["data"]["qq"]
        info = session.ctx["message"][2]["data"]["text"]
    except IndexError:
        await session.finish("转告登记失败")
    else:
        await session.finish("[CQ:at,qq={}]{}".format(into, info))


@on_command('retelling_refactoring', aliases=("发送到", "to"), only_to_me=False, permission=SUPERUSER)
async def retelling_refactoring(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        stripped_arg_list = stripped_arg.split(" ",1)
    try:
        to = int(stripped_arg_list[0])
        info = stripped_arg_list[1]
    except IndexError:
        await session.finish("转告登记失败")
    else:
        bot = get_bot()
        await bot.send_group_msg(group_id=to,
                                 message=info)


@on_command('get_group_list', aliases=("获取群列表",), only_to_me=False, permission=SUPERUSER)
async def get_group_list(session: CommandSession):
    bot = session.bot
    group_list = await bot.get_group_list()
    Ed, group_info = 0, "序号\t群号\t群名称\n"
    for i in group_list:
        Ed += 1
        group_info += "{}\t{}\t{}\n".format(Ed, i["group_id"], i["group_name"])
    await session.finish(group_info)


@on_command('print_global_variable', aliases=("输出全局变量",), only_to_me=False, permission=SUPERUSER)
async def print_global_variable(session: CommandSession):
    from config import TELL_TIME, DYNAMIC_SUBSCRIBE
    print(TELL_TIME)
    print(DYNAMIC_SUBSCRIBE)