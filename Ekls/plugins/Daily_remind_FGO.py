from datetime import datetime

import time
import nonebot
import pytz


from aiocqhttp.exceptions import Error as CQHttpError

from plugins.tool.date_box import sql_read


__plugin_name__ = "每日提醒"
__plugin_usage__ = """########################
今天的每日，你打了吗
########################
#
# 欲启用此功能请使用命令： 控制台"""

REMIND_TEXT = (
    "早上好,Master,今天是周一, 今天周回本开放「弓阶修炼场」,「收集火种(枪杀)」。\nο(=•ω＜=)ρ⌒☆",
    "早上好,Master,今天是周二, 今天周回本开放「枪阶修炼场」,「收集火种(剑骑)」。\nο(=•ω＜=)ρ⌒☆",
    "早上好,Master,今天是周三, 今天周回本开放「狂阶修炼场」,「收集火种(弓术)」。\nο(=•ω＜=)ρ⌒☆",
    "早上好,Master,今天是周四, 今天周回本开放「骑阶修炼场」,「收集火种(枪杀)」。\nο(=•ω＜=)ρ⌒☆",
    "早上好,Master,今天是周五, 今天周回本开放「术阶修炼场」,「收集火种(剑骑)」。\nο(=•ω＜=)ρ⌒☆",
    "早上好,Master,今天是周六, 今天周回本开放「杀阶修炼场」,「收集火种(弓术)」。\nο(=•ω＜=)ρ⌒☆",
    "早上好,Master,今天是周日, 今天周回本开放「剑阶修炼场」,「收集火种(All)」。\nο(=•ω＜=)ρ⌒☆",
    )
@nonebot.scheduler.scheduled_job('cron', hour='12', minute='30')  # 整点执行
#@nonebot.scheduler.scheduled_job('interval', seconds=10)    # 测试执行
async def _():
    bot = nonebot.get_bot()
    # await bot.send_group_msg(group_id=580695689, message='测试执行')
    try:    
        group_list = sql_read("User.db", "group_info", "Daily_remind_FGO", 1.0, field = "group_id", in_where = True)
        if group_list:
            week = time.localtime(time.time()).tm_wday
            week -= 1
            for group_id in group_list:
              await bot.send_group_msg(group_id=group_id[0], message=REMIND_TEXT[week])
    except CQHttpError:
        pass