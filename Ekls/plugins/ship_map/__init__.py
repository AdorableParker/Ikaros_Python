from nonebot import on_command, CommandSession
from nonebot.command.argfilter.extractors import extract_text
from nonebot.command.argfilter.validators import not_empty
from .positioning_coordinates import al_query_name, al_query_coordinate
from plugins.tool import reto



__plugin_name__ = "打捞定位"
__plugin_usage__ = """------ship_map------
命令关键字："打捞定位"
命令输入格式：

打捞定位 <船名|地图坐标>

效果：返回对应的船名列表或者地图坐标列表
########################"""


@on_command('ship_map', aliases=("打捞定位",), only_to_me=False)
async def ship_map (session: CommandSession):
    key = session.get('key', prompt='请输入索引信息', arg_filters=[extract_text, not_empty('索引不能为空哦')])
    time_key = reto.r2n(key, [r"\d*?\:\d"])
    if time_key:
        info = await al_query_name(time_key)
    else:
        info = await al_query_coordinate(key.upper())

    await session.finish(info, at_sender=True)


@construction_info.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['key'] = stripped_arg    
        return
    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
