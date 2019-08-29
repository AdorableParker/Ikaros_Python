from nonebot import on_notice, NoticeSession
from nonebot.helpers import render_expression
from plugins.tool.date_box import sql_delete

__plugin_name__ = "退群清理数据库"
__plugin_usage__ = "本功能为内置清理功能，将自动触发"

# 将函数注册为群成员减少通知处理器
@on_notice('group_decrease')
async def _(session: NoticeSession):
    if session.ctx["sub_type"] == "kick_me":
        sql_delete("User.db", "group_info", "group_id = {}".format(session.ctx["group_id"]))