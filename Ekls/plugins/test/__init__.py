# -*— coding: utf-8 -*-
"""
# 测试模块
"""

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand


# on_command 装饰器将函数声明为一个命令处理器
@on_command('test', aliases=("测试"), only_to_me=False)
async def test(session: CommandSession):
    # 向用户发送信息
    echo = ""
    for i in range(-10, 214):
        echo_info = "[CQ:face,id={}]".format(i)
        echo += "\t{0}\t{1}".format(echo_info, i)
        if not i%3:
            echo += "\n"
    await session.send(echo)