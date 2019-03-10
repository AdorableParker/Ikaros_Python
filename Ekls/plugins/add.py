from nonebot import on_notice, NoticeSession


__plugin_name__ = "迎新"
__plugin_usage__ = """
########################
#                      #
#     大佬又在装萌新了    #
#                      #
########################
"""


# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    if session.ctx['group_id'] == 463222048:
        await session.send('新来的大佬，先晒个秃头，以证船坞')
    elif session.ctx['group_id'] == 787211538:
        await session.send('是大佬！啊，大佬！啊！我死了')
