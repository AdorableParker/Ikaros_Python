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
    try:
        update_info = await crawler.update2out()
    except requests.exceptions.ConnectionError:
        update_info = "由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。"
    # 向用户发送信息
    # print(update_bilibili)
    await session.finish(update_info)