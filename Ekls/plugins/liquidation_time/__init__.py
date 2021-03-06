from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import render_expression

__plugin_name__ = "SIN"
__plugin_usage__ = """------liquidation_time------
Envy
Lust
Greed
Pride
Wrath
Sloth
Gluttony
########################"""

EXPL = ("好了，来细数你的罪恶吧",
        "好好想想你过去的所作所为",
        "阁下需要好好静一静",
        "主会宽恕你的",
        "这也是计划的一部分？",
        "在被禁言的边缘反复试探"
        )
EXRE = ("我伊卡洛斯又回来了",
        "为什么要禁言我",
        "可怜，弱小，又无助",
        "NMD，WSM",
        "我错了，下次还敢",
        "今天被禁言了，先记下来",
        "╥﹏╥...",
        "狗管理又欺负我，拿小本本记下了  ╥﹏╥"
       )

# 注册一个仅内部使用的命令，不需要 aliases
@on_command('liquidation_time')
async def liquidation_time(session: CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    await session.finish(render_expression(EXPL))


@on_natural_language(keywords={"被管理员禁言"}, only_to_me=False)
async def _(session: NLPSession):
    if session.ctx['user_id'] == 1000000:
        return IntentCommand(90.0, 'liquidation_time')

# 注册一个仅内部使用的命令，不需要 aliases
@on_command('emancipation')
async def emancipation(session: CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    await session.finish(render_expression(EXRE))


@on_natural_language(keywords={"(2951899724) 被管理员解除禁言"}, only_to_me=False)
async def _(session: NLPSession):
    if session.ctx['user_id'] == 1000000:
        return IntentCommand(90.0, 'emancipation')