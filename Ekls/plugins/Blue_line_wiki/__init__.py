# -*— coding: utf-8 -*-
"""
# 查询动态 命令
"""

from nonebot import on_command, CommandSession
from .get_ranking import get_equipment_list, get_srength_list


__plugin_name__ = "测评榜"
__plugin_usage__ = """
------equipment_ranking------
命令关键字："装备榜单", "装备榜", "装备排行榜"

效果：装备强度测评榜
########################

------srength_ranking------
命令关键字："强度榜单", "强度榜", "舰娘强度榜", "舰娘排行榜"

效果：舰娘强度测评榜
########################
"""


# on_command 装饰器将函数声明为一个命令处理器
@on_command('equipment_ranking', aliases=("装备榜单", "装备榜", "装备排行榜"), only_to_me=False)
async def equipment_ranking(session: CommandSession):
    # 获取B博信息
    url, info = await get_equipment_list()
    # 向用户发送信息
    # print(update_bilibili)
    await session.finish("装备榜单：\n{}\n{}".format(url, info))

# on_command 装饰器将函数声明为一个命令处理器
@on_command('srength_ranking', aliases=("强度榜单", "强度榜", "舰娘强度榜", "舰娘排行榜"), only_to_me=False)
async def srength_ranking(session: CommandSession):
    # 获取B博信息
    url, info = await get_srength_list()
    # 向用户发送信息
    # print(update_bilibili)
    await session.finish("强度榜单：\n{}\n{}".format(url, info))
