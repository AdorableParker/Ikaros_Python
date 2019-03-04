# -*— coding: utf-8 -*-
"""
# 查询动态 命令
"""

from nonebot import on_command, CommandSession

from plugins.tool import crawler
from .x import get_ing


__plugin_name__ = "碧蓝航线动态获取"
__plugin_usage__ = """
------update_bilibili------
关键字："小加加", "B博更新", "b博更新"

效果：锉刀怪又gū了？让我康康

########################

关键字："各服进度", "活动进度", "各服排名", "活动排行", "各区排行", "各区排名", "各服排行", "各区进度"

此功能仅在全服活动期间开放
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


# on_command 装饰器将函数声明为一个命令处理器
@on_command('update_get_ing', aliases=("各服进度", "活动进度", "各服排名", "活动排行", "各区排行", "各区排名", "各服排行", "各区进度"), only_to_me=False)
async def update_get_ing(session: CommandSession):
    # 活动期临时功能
    try:
        text = get_ing()
    except:
        text = "由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。"
    await session.finish(text)