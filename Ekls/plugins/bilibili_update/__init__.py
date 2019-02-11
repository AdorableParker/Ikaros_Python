# -*— coding: utf-8 -*-
"""
# 查询动态 命令
"""

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

from .crawler import update2out


# on_command 装饰器将函数声明为一个命令处理器
@on_command('update_bilibili', aliases=("小加加", "B博更新", "b博更新"), only_to_me=False)
async def update_bilibili(session: CommandSession):
    # 获取B博信息
    update_info = await update2out()
    # 向用户发送信息
    # print(update_bilibili)
    await session.send(update_info)