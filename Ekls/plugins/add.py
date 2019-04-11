from nonebot import on_notice, NoticeSession
from nonebot.helpers import render_expression


__plugin_name__ = "迎新"
__plugin_usage__ = """
########################
#                      #
#    大佬又在装萌新了    #
#                      #
########################
"""

GROUP_ID_LIST = (463222048, 787211538, 476957090)
EXL = ('新来的大佬，先晒个秃头，以证船坞', 
       '是大佬！啊，大佬！啊！我死了',
       '群地位-1'
        )
# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    if session.ctx['group_id'] in GROUP_ID_LIST:
        await session.finish(render_expression(EXL))