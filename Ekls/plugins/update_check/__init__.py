from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

from .get_update import update_check


__plugin_name__ = "动态更新"
__plugin_usage__ = """
########################
今天有没有被指挥官偷瞄呢(:3_ヽ)_
\t\t————萨拉托加
########################
"""


@nonebot.scheduler.scheduled_job('cron', hour='*', minute="0/20")  # 每半小时执行
# @nonebot.scheduler.scheduled_job('interval', minutes=1)    # 间隔一分钟执行
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    print("动态更新执行")
    try:
        update_info = update_check()
        
        if update_info[0]:
            # 碧蓝群
            await bot.send_group_msg(group_id=463222048, message=update_info[1])
            await bot.send_group_msg(group_id=787211538, message=update_info[1])

    except CQHttpError:
            await bot.send_group_msg(group_id=463222048, message="更新动态失败")
            await bot.send_group_msg(group_id=787211538, message="更新动态失败")

if __name__ == "__main__":
    update_info = update_check()
    print(update_info)