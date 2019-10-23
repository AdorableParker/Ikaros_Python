from datetime import datetime
import time
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

from .get_update import update_check
from plugins.tool.date_box import sql_read
from plugins.rendering import render
from config import SUPERUSERS

__plugin_name__ = "动态更新"
__plugin_usage__ = """########################
今天有没有被指挥官偷瞄呢(:3_ヽ)_
\t\t————萨拉托加
########################
#
# 欲启用此功能请使用命令： 控制台"""


@nonebot.scheduler.scheduled_job('cron', hour='*', minute="1/9")  # 第一分钟开始每九分钟执行一次
#@nonebot.scheduler.scheduled_job('interval', seconds=30)    # 间隔三十秒执行
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))

    # 火星时报
    group_list = sql_read("User.db", "group_info", "Sara_news", 1.0, field = "group_id", in_where = True)
    if group_list:
        update_info = update_check('233114659')
        if update_info[0]:
            for group_id in group_list:
                try:
                    await bot.send_group_msg(group_id=group_id[0], message=update_info[1])
                except CQHttpError as err:
                    await notice(bot, group_id[0], err)


    # 标枪快讯
    group_list = sql_read("User.db", "group_info", "Javelin_news", 1.0, field = "group_id", in_where = True)
    if group_list:
        update_info = update_check('300123440')
        if update_info[0]:
            #update_info = "{}\n————————\n百度机翻如下：\n\n{}".format(update_info[1], render(update_info[1]))
            for group_id in group_list:
                try:
                    await bot.send_group_msg(group_id=group_id[0], message=update_info[1])
                except CQHttpError as err:
                    await notice(bot, group_id[0], err)


    # 罗德岛线报
    group_list = sql_read("User.db", "group_info", "Arknights", 1.0, field = "group_id", in_where = True)
    if group_list:
        update_info = update_check('161775300')
        if update_info[0]:
            for group_id in group_list:
                try:
                    await bot.send_group_msg(group_id=group_id[0], message=update_info[1])
                except CQHttpError as err:
                    await notice(bot, group_id[0], err)

async def notice(bot, group_id, err):
        if err.retcode == -34:
            print("由于被禁言而发送失败")
        else:
            for i in SUPERUSERS:
                await bot.send_private_msg(user_id=i, message="公告发送异常，群号：{}\n错误信息：{}".format(group_id, err.retcode))

if __name__ == "__main__":
    update_info = update_check()
    print(update_info)