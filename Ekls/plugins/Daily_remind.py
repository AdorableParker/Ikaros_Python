from datetime import datetime

import time
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

from plugins.tool.date_box import sql_read


__plugin_name__ = "每日提醒"
__plugin_usage__ = """########################
今天的每日，你打了吗
########################"""

REMIND_TEXT = (
    "今天是周{}哦,每日开放的是「战术研修」「商船护送」，困难也记得打呢。各位指挥官晚安咯\nο(=•ω＜=)ρ⌒☆",
    "今天是周{}哦,每日开放的是「战术研修」「海域突进」，困难也记得打呢。各位指挥官晚安咯\nο(=•ω＜=)ρ⌒☆",
    "今天是周{}哦,每日开放的是「战术研修」「斩首行动」，困难也记得打呢。各位指挥官晚安咯\nο(=•ω＜=)ρ⌒☆",
    "今天是周{}哦,每日全部模式开放，困难也记得打呢。各位指挥官晚安咯\nο(=•ω＜=)ρ⌒☆",
    )
ZH_CODE = (
    ("四", "一"),
    ("五", "二"),
    ("六", "三"),
    ("日")
    )
@nonebot.scheduler.scheduled_job('cron', hour='*', minute='30')  # 整点执行
#@nonebot.scheduler.scheduled_job('interval', seconds=10)    # 测试执行
async def _():
    bot = nonebot.get_bot()
    # await bot.send_group_msg(group_id=580695689, message='测试执行')
    try:    
        group_list = sql_read("User.db", "group_info", "Daily_remind", 1.0, field = "group_id", in_where = True)
        if group_list:
            week = time.localtime(time.time()).tm_wday
            if week > 2:
                week -= 3
            else:
                flag = True

            for group_id in group_list:
              await bot.send_group_msg(group_id=group_id[0], message=REMIND_TEXT[week].format(ZH_CODE[week][flag]))
    except CQHttpError:
        pass