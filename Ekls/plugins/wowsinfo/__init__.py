# -*— coding: utf-8 -*-

from nonebot import on_command, CommandSession
from .wowsapi import infoInquire, getshipinfo


__plugin_name__ = "wowsinfo"
__plugin_usage__ = """------wowsinfo------
命令关键字："wowsinfo"
命令输入格式：

wowsinfo <账号名>#<游戏模式>[#船名]
# 可选以下模式，默认匹配模式

"人机"    “匹配”    "军团"
"单排"    "双排"    "三排"
"单人剧情"  "组队剧情"  "组队困难剧情"

# 查询游戏服务器很卡，所以理解一下
# 目前只支持亚服账号
# 新项目上线bug多是正常的
# 船名参数是可选的
# 用于查询该账户的那一艘船的战绩信息
########################"""


@on_command('wowsinfo', aliases=("wowsinfo",), only_to_me=False)
async def wowsinfo(session: CommandSession):
    name = session.get('name', prompt='输入需查询账号名<目前只支持亚服>')
    mods = session.get('mods', prompt='输入需查询游戏模式<"人机" “匹配” "军团" "单排" "双排" "三排" "单人剧情" "组队剧情" "组队困难剧情">')
    shipname = session.get('shipname', prompt='输入需查询船名')
    await session.send("正在查询服务器")

    if not shipname:
        outinfo, err = await infoInquire(name, mods)
        if err:
            info = ""
            for i in outinfo:
                info += "\n{}: {}".format(i, outinfo[i])
            await session.finish(info, at_sender=True)
        else:
            await session.finish(outinfo, at_sender=True)
    else:
        outinfo, err = await getshipinfo(name, shipname, mods)
        if not err:
            for num, resultdict in enumerate(outinfo,start=1):
                outinfo = ''
                for i in resultdict:
                    outinfo += "{}: {}\n".format(i,resultdict[i])
                await session.send("{}当前 第 {} 条".format(outinfo, num))
            await session.finish("全部查询已输出", at_sender=True)
        else:
            await session.finish(outinfo, at_sender=True)

@wowsinfo.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            stripped_arg_list = stripped_arg.split("#", 2)
            if len(stripped_arg_list) == 3:
                session.state['name'] = stripped_arg_list[0]
                session.state['mods'] = stripped_arg_list[1]
                session.state['shipname'] = stripped_arg_list[2]
            elif len(stripped_arg_list) == 2:
                session.state['name'] = stripped_arg_list[0]
                session.state['mods'] = stripped_arg_list[1]
                session.state['shipname'] = ""
            else:
                session.state['name'] = stripped_arg
                session.state['mods'] = ""
                session.state['shipname'] = ""
        return

    if not stripped_arg:
        if not session.state.get('name'):
            session.pause('账号名不能为空呢，请重新输入')
    session.state[session.current_key] = stripped_arg