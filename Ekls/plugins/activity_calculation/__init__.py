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
    user_defined = session.get('user_defined', prompt='请输入已刷点数')
    user_defined = int(user_defined) if user_defined else False 
    result = await progress_calculat(content, user_defined)
    await session.finish(result, at_sender=True)


@activity.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        stripped_arg_list = stripped_arg.split("#",1)
        if len(stripped_arg_list) > 1:
            session.state['content'] = stripped_arg_list[0]
            session.state['user_defined'] = stripped_arg_list[1]
            await session.send('自定义目标已设定，仅此次计算时生效')
        else:
            session.state['content'] = stripped_arg
            session.state['user_defined'] = ""
    else:
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('请输入已刷点数')

    session.state[session.current_key] = stripped_arg

