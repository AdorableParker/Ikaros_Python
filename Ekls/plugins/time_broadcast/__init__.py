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
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        # 碧蓝群
        await bot.send_group_msg(group_id=463222048,
                                 message=line())
        # 咕咕群
        now_time = time.strftime('%H',time.localtime(time.time()))
        await bot.send_group_msg(group_id=670518695,
                                 message='现在{}点咯！'.format(now_time))
        await bot.send_group_msg(group_id=483985370,
                                 message='现在{}点咯！'.format(now_time))
    except CQHttpError:
        pass
