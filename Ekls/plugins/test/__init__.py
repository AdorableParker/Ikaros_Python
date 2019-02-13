# -*— coding: utf-8 -*-
"""
# 测试模块
"""

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand



__plugin_name__ = "测试模块"
__plugin_usage__ = """
------test------
命令关键字："测试"

效果：打印出一张又臭又长的 表情——代号 对应表
########################
"""


# on_command 装饰器将函数声明为一个命令处理器
@on_command('test', aliases=("测试"), only_to_me=False)
async def test(session: CommandSession):
    # 向用户发送信息
    echo = ""
    for i in range(215):
        echo_info = "[CQ:face,id={}]".format(i)
        echo += "\t{0}\t{1}".format(echo_info, i)
        if not i%3:
            echo += "\n"
    await session.send(echo)