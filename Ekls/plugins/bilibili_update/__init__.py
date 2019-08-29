# -*— coding: utf-8 -*-
"""
# 查询动态 命令
"""

from nonebot import on_command, CommandSession

from plugins.tool import crawler
from plugins.rendering import render
import requests

__plugin_name__ = "B站动态获取"
__plugin_usage__ = """------update_bilibili------
关键字："小加加", "火星加", "B博更新", "b博更新"

效果：锉刀怪又gū了？让我康康

########################

------bilibili_jp_Twitter------
关键字："转推姬", "碧蓝日推"

效果：这特么是什么东西

########################

------update_bilibili_Arknights------
关键字："罗德岛线报", "方舟公告", "方舟B博", "阿米娅"

效果：博士，您还有许多事情需要处理，现在还不能休息哦。

#
# 欲启用自动更新模式请使用命令 "控制台" 获取更多信息"""


# on_command 装饰器将函数声明为一个命令处理器
@on_command('update_bilibili', aliases=("小加加", "火星加","B博更新", "b博更新"), only_to_me=False)
async def update_bilibili(session: CommandSession):
    # 获取B博信息
    stripped_arg = session.current_arg_text.strip()
    try:
        stripped_arg = int(stripped_arg) if stripped_arg else 0
        if stripped_arg > 10:
            await session.send('最多只能往前10条哦')
            stripped_arg = 10
        elif stripped_arg < 0:
            await session.send('未来的事情还没发生呢')
            stripped_arg = 0
        update_info = await crawler.update2out("233114659", stripped_arg) #"300123440"
    except requests.exceptions.ConnectionError:
        update_info = "由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。"
    except ValueError:
        update_info = "请不要填些奇奇怪怪的东西"
    # 向用户发送信息
    # print(update_bilibili)
    await session.finish(update_info)


@on_command('update_bilibili_jp_Twitter', aliases=("转推姬", "碧蓝日推"), only_to_me=False)
async def update_bilibili_jp_Twitter(session: CommandSession):
    # 获取B博信息
    try:
        update_info = await crawler.update2out("300123440")
    except:
        update_info = "由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。"
    # 向用户发送信息
    # print(update_bilibili)
    out_info = "{}\n————————\n百度机翻如下：\n\n{}".format(update_info, render(update_info))

    await session.finish(out_info)


@on_command('update_bilibili_Arknights', aliases=("罗德岛线报", "方舟公告","方舟B博", "阿米娅"), only_to_me=False)
async def update_bilibili_Arknights(session: CommandSession):
    # 获取B博信息
    stripped_arg = session.current_arg_text.strip()
    try:
        stripped_arg = int(stripped_arg) if stripped_arg else 0
        if stripped_arg > 10:
            await session.send('最多只能往前10条哦')
            stripped_arg = 10
        elif stripped_arg < 0:
            await session.send('未来的事情还没发生呢')
            stripped_arg = 0
        update_info = await crawler.update2out("161775300", stripped_arg)
    except requests.exceptions.ConnectionError:
        update_info = "由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。"
    except ValueError:
        update_info = "请不要填些奇奇怪怪的东西"
    # 向用户发送信息
    # print(update_bilibili)
    await session.finish(update_info)