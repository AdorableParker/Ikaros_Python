from nonebot import on_command, CommandSession, get_bot
from nonebot.permission import SUPERUSER

from .miscellaneous_function import string_cover as str_co
from .miscellaneous_function import change_everything as ce
from plugins.tool.date_box import sql_rewrite, sql_read, sql_write, look

__plugin_name__ = "控制台"
__plugin_usage__ = """------terminal_console------
命令关键字："控制台", "终端"

$ 获取群列表
$ 汇报各群功能配置情况
$ 发送到群 <目标> <内容>
$ 改变复读姬状态 [目标]
$ 改变开火许可状态 [目标]
$ 改变火星时报订阅状态 [目标]
$ 改变标枪快讯订阅状态 [目标]
$ 改变报时鸟状态 [目标]
$ 改变报时鸟_舰C版状态 [目标]
$"""



@on_command('terminal_console', aliases=("控制台", "终端"), only_to_me=False, permission=SUPERUSER)
async def admin_terminal_console(session: CommandSession):
    
    await session.finish(__plugin_usage__)



@on_command('update_group_list', aliases=("更新群列表",), only_to_me=False, permission=SUPERUSER)
async def get_group_list(session: CommandSession):
    bot = session.bot
    group_list = await bot.get_group_list()
    Ed, group_info = 0, "序号\t群号\t群名称"
    for i in group_list:
        Ed += 1
        if not sql_rewrite("User.db", "group_info", "group_id", i["group_id"], "id", Ed): # 序号改变
            sql_write("User.db", "group_info", (Ed, i["group_id"]))  # 无则添加
        group_info += "\n{}\t{}\t{}".format(Ed, str_co(i["group_id"],"*"), str_co(i["group_name"], "#")) # 加入掩码
    await session.finish(group_info)



@on_command('print_global_variable', aliases=("汇报各群功能配置情况",), only_to_me=False, permission=SUPERUSER)
async def print_global_variable(session: CommandSession):
    print(look("User.db", "group_info"))
    await session.finish("已输出到控制台")


@on_command('retelling_refactoring', aliases=("发送到群", "to"), only_to_me=False, permission=SUPERUSER)
async def retelling_refactoring(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        stripped_arg_list = stripped_arg.split(" ",1)
        if stripped_arg_list[0].startswith("#"):
            to = int(sql_read("User.db", "group_info", "id", stripped_arg_list[0].lstrip("#"))[0][1])       
        else:
            to = int(stripped_arg_list[0])
        info = stripped_arg_list[1]
        bot = get_bot()
        await bot.send_group_msg(group_id=to, message=info)


@on_command('repeat_alter', aliases=("改变复读姬状态",), only_to_me=False, permission=SUPERUSER)
async def repeat_alter(session: CommandSession):
    intent, echo = await ce(session, "repeat")
    await session.finish("复读姬原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('fire_alter', aliases=("改变开火许可状态",), only_to_me=False, permission=SUPERUSER)
async def fire_alter(session: CommandSession):
    intent, echo = await ce(session, "fire")
    await session.finish("开火权限原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Sara_news_alter', aliases=("改变火星时报订阅状态",), only_to_me=False, permission=SUPERUSER)
async def Sara_news_alter(session: CommandSession):
    intent, echo = await ce(session, "Sara_news")
    await session.finish("火星时报订阅原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Javelin_news_alter', aliases=("改变标枪快讯订阅状态",), only_to_me=False, permission=SUPERUSER)
async def Javelin_news_alter(session: CommandSession):
    intent, echo = await ce(session, "Javelin_news")
    await session.finish("标枪快讯订阅原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Call_bell_alter', aliases=("改变报时鸟状态",), only_to_me=False, permission=SUPERUSER)
async def Call_bell_alter(session: CommandSession):
    intent, echo, group_id = await ce(session, "Call_bell", True)
    if echo:
        sql_rewrite("User.db", "group_info", "group_id", group_id, "Call_bell_AZ", False)
    await session.finish("报时鸟原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Call_bell_AZ_alter', aliases=("改变报时鸟_舰C版状态",), only_to_me=False, permission=SUPERUSER)
async def Call_bell_AZ_alter(session: CommandSession):
    intent, echo, group_id = await ce(session, "Call_bell_AZ", True)
    if echo:
        sql_rewrite("User.db", "group_info", "group_id", group_id, "Call_bell", False)
    await session.finish("舰C版报时鸟原状态为 {}\n现状态已改为 {}".format(intent, echo))