# -*— coding: utf-8 -*-
"""
# 查询动态 命令
"""

from nonebot import on_command, CommandSession

from plugins.tool import crawler


__plugin_name__ = "碧蓝航线动态获取"
__plugin_usage__ = """
------update_bilibili------
关键字："小加加", "B博更新", "b博更新"

效果：锉刀怪又gū了？让我康康

########################
"""


# on_command 装饰器将函数声明为一个命令处理器
@on_command('update_bilibili', aliases=("小加加", "B博更新", "b博更新"), only_to_me=False)
async def update_bilibili(session: CommandSession):
    # 获取B博信息
    update_info = await crawler.update2out()
    # 向用户发送信息
    # print(update_bilibili)
    await session.send(update_info)