from nonebot import on_command, CommandSession

from .al_producetime_query import al_query_time, al_query_name
from . import reto

__plugin_name__ = "建造时间查询"
__plugin_usage__ = """------construction_info------
命令关键字："建造时间查询", "建造时间", "建造查询"
命令输入格式：

建造时间查询 <时间|船名>

效果：返回数据库中，符合的船名和时间
########################"""


@on_command('construction_info', aliases=("建造时间查询", "建造时间", "建造查询"), only_to_me=False)
async def construction_info (session: CommandSession):
    key = session.get('key')
    time_key = reto.r2n(key, [r"\d\:\d\d"])
    if time_key:
        info = await al_query_name(time_key)
    else:
        info = await al_query_time(key.upper())
    await session.finish("{}".format(info), at_sender=True)


@construction_info.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            stripped_arg = stripped_arg.replace('：', ':')
            session.state['key'] = stripped_arg    
        return
    if not stripped_arg:
        session.pause('索引不能为空哦')
    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
