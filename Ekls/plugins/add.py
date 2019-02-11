from nonebot import on_notice, NoticeSession


# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    if session.ctx['group_id'] == 463222048:
    # if True:
        # print(session.ctx['group_id'])
        await session.send('新来的大佬，先晒个秃头，以证船坞')
