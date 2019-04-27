from datetime import datetime

import time
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

from .time_word import line

from plugins.tool.date_box import sql_read


__plugin_name__ = "整点报时"
__plugin_usage__ = """########################
伊卡洛斯 为您报时
########################"""


@nonebot.scheduler.scheduled_job('cron', hour='*')  # 整点执行
# @nonebot.scheduler.scheduled_job('interval', seconds=10)    # 测试执行
async def _():

    
    bot = nonebot.get_bot()
    # await bot.send_group_msg(group_id=580695689, message='测试执行')
    try:    
        group_list = sql_read("User.db", "group_info", "Call_bell_AZ", True, field = "group_id", in_where = True)
        if group_list:
            time_line = line()
            for group_id in group_list:
              await bot.send_group_msg(group_id=group_id, message=time_line)


        group_list = sql_read("User.db", "group_info", "Call_bell", True, field = "group_id", in_where = True)
        if group_list:
            now_time = time.strftime('%H',time.localtime(time.time()))
            for group_id in group_list:
                await bot.send_group_msg(group_id=group_id, message='现在{}点咯！'.format(now_time))
    except CQHttpError:
        pass