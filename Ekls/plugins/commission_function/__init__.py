import time
import nonebot
from plugins.tool.date_box import look, sql_delete, sql_read


__plugin_name__ = "定制功能"
__plugin_usage__ = """########################
专门给私人的群定制的群管功能，不开放其他群使用
########################"""


@nonebot.scheduler.scheduled_job('cron', hour='0')  # 零点执行
#@nonebot.scheduler.scheduled_job('interval', seconds=10)    # 测试执行
async def _():
    bot = nonebot.get_bot()

    kill_list = look("User.db", "kill_list")
    for id, timecode in kill_list:
        if time.time() - timecode > 7200:
            await bot.set_group_kick(group_id=578182492, user_id=id)
            sql_delete("User.db", "kill_list","ID = {}".format(id))
            await bot.send_group_msg(group_id=578182492, message='QID:{}因 入群后超过两小时时间未发言 已被移出本群'.format(id))