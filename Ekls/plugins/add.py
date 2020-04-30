from nonebot import on_notice , NoticeSession
from nonebot.helpers import render_expression
from plugins.tool.date_box import sql_read, sql_write
import time

__plugin_name__ = "迎新"
__plugin_usage__ = """########################
#                      #
#    大佬又在装萌新了    #
#                      #
########################
#
# 欲启用此功能请使用命令： 控制台"""


EXL = ('是大佬！啊，大佬！啊！我死了',
       '群地位-1',
       '您好，我是本群PDA——伊卡洛斯\n本群最新《群员管理办法》已经再群公告中展示\n具体条例请自行查看，感谢您的配合'
        )
# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    if sql_read("User.db", "group_info", "group_id", session.ctx["group_id"], field = "New_add", in_where = True)[0][0]:
        await session.send(render_expression(EXL))
