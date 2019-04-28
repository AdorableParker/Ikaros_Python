from datetime import datetime
import time
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

from .get_update import update_check

from plugins.tool.date_box import sql_read
__plugin_name__ = "动态更新"
__plugin_usage__ = """########################
今天有没有被指挥官偷瞄呢(:3_ヽ)_
\t\t————萨拉托加
########################"""


@nonebot.scheduler.scheduled_job('cron', hour='*', minute="0/20")  # 每半小时执行
#@nonebot.scheduler.scheduled_job('interval', seconds=60)    # 间隔一分钟执行
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    # 火星时报
    group_list = sql_read("User.db", "group_info", "Sara_news", 1.0, field = "group_id", in_where = True)
    if not group_list:
        update_info = update_check('233114659')
        for group_id in group_list:
            try:
                await bot.send_group_msg(group_id=group_id, message=update_info[1])
            except:
                for group_id in group_list:
                    await bot.send_group_msg(group_id=group_id, message="更新动态失败")
    # 标枪快讯
    group_list = sql_read("User.db", "group_info", "Javelin_news", 1.0, field = "group_id", in_where = True)
    if not group_list:
        update_info = update_check('300123440')
        for group_id in group_list:
            try:
                await bot.send_group_msg(group_id=group_id, message=update_info[1])
            except:
                for group_id in group_list:
                    await bot.send_group_msg(group_id=group_id, message="更新动态失败")

if __name__ == "__main__":
    update_info = update_check()
    print(update_info)