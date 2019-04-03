from datetime import datetime
import time
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
# 群列表
GROUP_LIST = (
    463222048,
    787211538,
    476957090
    )
# 源列表
UID_LIST = (
    "300123440",
    "233114659"
    )


@nonebot.scheduler.scheduled_job('cron', hour='*', minute="0/20")  # 每半小时执行
#@nonebot.scheduler.scheduled_job('interval', minutes=1)    # 间隔一分钟执行
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    print("{} 动态更新执行".format(time.strftime('%H%M%S',time.localtime(time.time()))))
    for uid in UID_LIST:
        try:
            update_info = update_check(uid)
            if update_info[0]:
                # 碧蓝群
                for group_id in GROUP_LIST:
                    await bot.send_group_msg(group_id=group_id, message=update_info[1])
        except:
            for group_id in GROUP_LIST:
                await bot.send_group_msg(group_id=group_id, message="更新动态失败")
        else:
            print("{} {}更新完成 ".format(time.strftime('%H%M%S',time.localtime(time.time())), uid))
    else:
        print("{} 动态更新全部完成 ".format(time.strftime('%H%M%S',time.localtime(time.time()))))

if __name__ == "__main__":
    update_info = update_check()
    print(update_info)