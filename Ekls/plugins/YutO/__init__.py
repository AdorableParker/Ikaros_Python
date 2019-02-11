from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand


@on_command('open_fire')
async def open_fire(session: CommandSession):
    if session.ctx['user_id'] == 798864550:
        await session.send('I！YUTO！TM BURST-FORTH ！')
    else:
        await session.send('你涉嫌无证射爆，请立刻中止行为，接受检查！！')

@on_command('i_want')
async def i_want(session: CommandSession):
    if session.ctx['user_id'] == 798864550:
        await session.send("我懂，你又想射爆了对吧[CQ:face,id=179]")

# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(keywords={'射爆', '社保'}, only_to_me=False)
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(100.0, 'open_fire')

@on_natural_language(keywords={'我想'}, only_to_me=False)
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(100, 'i_want')