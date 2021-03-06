from nonebot import on_command, CommandSession, get_bot
from nonebot.permission import SUPERUSER, GROUP_ADMIN

from .miscellaneous_function import string_cover as str_co
from .miscellaneous_function import change_everything as ce
from plugins.tool.date_box import sql_rewrite, sql_read, sql_write, look

__plugin_name__ = "控制台"
__plugin_usage__ = """------terminal_console------
命令关键字："控制台", "终端"

&内部管理员执行有效&

$ 汇报各群功能配置情况
$ 发送公告 <内容>
$ 发送到群 <目标> <内容>

&群管理员执行有效&

$ 改变复读姬状态 [目标]
$ 改变开火许可状态 [目标]
$ 改变火星时报订阅状态 [目标]
$ 改变标枪快讯订阅状态 [目标]
$ 改变罗德岛线报订阅状态 [目标]
$ 改变报时鸟状态 [目标]
$ 改变报时鸟_舰C版状态 [目标]
$ 改变迎新功能状态 [目标]
$ 改变每日提醒_舰B版功能状态 [目标]
$ 改变每日提醒_FGO版功能状态 [目标]"""




@on_command('terminal_console', aliases=("控制台", "终端"), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def admin_terminal_console(session: CommandSession):
    await session.finish(__plugin_usage__)


@on_command('print_global_variable', aliases=("汇报各群功能配置情况",), only_to_me=False, permission=SUPERUSER)
async def print_global_variable(session: CommandSession):
    for i in look("User.db", "group_info"):
        print(i)
    await session.finish("已输出到控制台")


@on_command('send_announcement', aliases=("发送公告", "to_all"), only_to_me=False, permission=SUPERUSER)
async def send_announcement(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        group_list = await session.bot.get_group_list()
        bot = get_bot()
        for i in group_list:
            await bot.send_group_msg(group_id=i["group_id"], message=stripped_arg)


@on_command('send_to_group', aliases=("发送到群", "to"), only_to_me=False, permission=SUPERUSER)
async def send_to_group(session: CommandSession):
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


@on_command('repeat_alter', aliases=("改变复读姬状态",), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def repeat_alter(session: CommandSession):
    intent, echo = await ce(session, "repeat")
    await session.finish("复读姬原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('fire_alter', aliases=("改变开火许可状态",), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def fire_alter(session: CommandSession):
    intent, echo = await ce(session, "fire")
    await session.finish("开火权限原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Sara_news_alter', aliases=("改变火星时报订阅状态",), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def Sara_news_alter(session: CommandSession):
    intent, echo = await ce(session, "Sara_news")
    await session.finish("火星时报订阅原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Javelin_news_alter', aliases=("改变标枪快讯订阅状态",), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def Javelin_news_alter(session: CommandSession):
    intent, echo = await ce(session, "Javelin_news")
    await session.finish("标枪快讯订阅原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Arknights_alter', aliases=("改变罗德岛线报订阅状态",), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def Arknights_alter(session: CommandSession):
    intent, echo = await ce(session, "Arknights")
    await session.finish("罗德岛线报订阅原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Call_bell_alter', aliases=("改变报时鸟状态",), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def Call_bell_alter(session: CommandSession):
    intent, echo, group_id = await ce(session, "Call_bell", True)
    if echo:
        sql_rewrite("User.db", "group_info", "group_id", group_id, "Call_bell_AZ", 0)
    await session.finish("报时鸟原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Call_bell_AZ_alter', aliases=("改变报时鸟_舰C版状态",), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def Call_bell_AZ_alter(session: CommandSession):
    intent, echo, group_id = await ce(session, "Call_bell_AZ", True)
    if echo:
        sql_rewrite("User.db", "group_info", "group_id", group_id, "Call_bell", 0)
    await session.finish("舰C版报时鸟原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('New_add_alter', aliases=("改变迎新功能状态",), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def New_add_alter(session: CommandSession):
    intent, echo, group_id = await ce(session, "New_add", True)
    await session.finish("迎新功能原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Daily_remind_alter', aliases=("改变每日提醒_舰B版功能状态",), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def Daily_remind_alter(session: CommandSession):
    intent, echo, group_id = await ce(session, "Daily_remind_AzurLane", True)
    await session.finish("每日提醒_舰B版功能原状态为 {}\n现状态已改为 {}".format(intent, echo))


@on_command('Daily_remind_alter_FGO', aliases=("改变每日提醒_FGO版功能状态",), only_to_me=False, permission=SUPERUSER|GROUP_ADMIN)
async def Daily_remind_alter_FGO(session: CommandSession):
    intent, echo, group_id = await ce(session, "Daily_remind_FGO", True)
    await session.finish("每日提醒_FGO版功能原状态为 {}\n现状态已改为 {}".format(intent, echo))