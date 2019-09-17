from nonebot import on_command, CommandSession

from .code_conversion import code_name

__plugin_name__ = "重樱船名查询"
__plugin_usage__ = """------heavycherry_boat_name_query------
命令关键字："重樱船名查询", "重樱船名", "船名查询", "和谐名查询"
命令输入格式：

重樱船名 <船名>

效果：返回数据库中，符合的船名
########################"""


@on_command('heavycherry_boat_name_query', aliases=("重樱船名查询", "重樱船名", "船名查询", "和谐名查询"), only_to_me=False)
async def heavycherry_boat_name_query (session: CommandSession):
    key = session.get('key', prompt='需要查询的船名', arg_filters=[extract_text, not_empty('输入不能为空哦')])

    info = await code_name(key)
    if info[0]:
        await session.finish("{}".format(info[1]), at_sender=True)
    else:
        await session.finish("数据库中查无此船", at_sender=True)


@heavycherry_boat_name_query.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['key'] = stripped_arg    
        return
    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
