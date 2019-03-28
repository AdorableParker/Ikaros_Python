from nonebot import permission, on_command, CommandSession
from .activity_calculation import progress_calculat


__plugin_name__ = "碧蓝航线活动进度"
__plugin_usage__ = """
------activity------
命令关键字："活动进度", "进度计算", "奖池计算"
命令输入格式：

活动进度 <已刷点数>

效果：根据已刷点数，返回活动进度报告

########################
"""



# on_command 装饰器将函数声明为一个命令处理器
@on_command('activity', aliases=("活动进度", "进度计算", "奖池计算"), only_to_me=False)
async def activity(session: CommandSession):
    # 向用户发送信息
    content = session.get('content', prompt='请输入已刷点数')
    result = await progress_calculat(content)
    await session.finish(result, at_sender=True)


@activity.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['content'] = stripped_arg
        return

    if not stripped_arg:
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('请重新输入')

    session.state[session.current_key] = stripped_arg

