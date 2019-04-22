from datetime import datetime

import time
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

from .time_word import line


__plugin_name__ = "整点报时"
__plugin_usage__ = """
########################
伊卡洛斯 为您报时
########################
"""


@nonebot.scheduler.scheduled_job('cron', hour='*')  # 整点执行
# @nonebot.scheduler.scheduled_job('interval', minutes=1)    # 间隔一分钟执行
async def _():
    bot = nonebot.get_bot()
    try:
        # 碧蓝群
        time_line = line()
        bilian_group_id_list = (463222048, 476957090)
        for group_id in bilian_group_id_list:
            await bot.send_group_msg(group_id=group_id, message=time_line)

        # 咕咕群
        group_id_list = (670518695, 483985370, 945098403)
        now_time = time.strftime('%H',time.localtime(time.time()))
        for group_id in group_id_list:
            await bot.send_group_msg(group_id=group_id, message='现在{}点咯！'.format(now_time))
    except CQHttpError:
        pass