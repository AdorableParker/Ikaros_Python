import json
from typing import Optional

import aiohttp
from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression

from .data_box import sql_rewrite, sql_read


__plugin_name__ = "复读姬"
__plugin_usage__ = """
------repeat------

人类的本质是什么？

给我把倒数第二个复读机砸了！
########################
"""


# 注册一个仅内部使用的命令，不需要 aliases
@on_command('repeat')
async def repeat(session: CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = session.state.get('message')

    reply = await get_repeat(session, message)
    if reply:
        # 如果调用
        # 转义会把消息中的某些特殊字符做转换，以避免 酷Q 将它们理解为 CQ 码
        await session.send(escape(reply))


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    # 以置信度 60.0 返回 tuling 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候触发命令
    return IntentCommand(60.0, 'repeat', args={'message': session.msg_text})


async def get_repeat(session: CommandSession, text: str) -> Optional[str]:
    # 查询数据库

    if not text:
        return None
    try:
        old_info, flag, user, old_user = sql_read("User.db", "repeat_info", "groupid", session.ctx["group_id"])[0][:4]
    except IndexError:
        # 初步判定为未添加复读
        pass
    else:
        if old_info == text:
            if flag == 1:
                sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "flag", 2)
            elif flag == 0:
                sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "flag", 1)
                text = False
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "old_userid", user)
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "userid", session.ctx["user_id"])
            return text
        else:
            if flag == 2:
                bot = session.bot
                try:
                    await bot.set_group_ban(group_id=session.ctx['group_id'], 
                                            user_id=old_user,
                                            duration=120)
                    await bot.set_group_ban(group_id=session.ctx['group_id'], 
                                            user_id=session.ctx['user_id'],
                                            duration=60)
                except CQHttpError:
                    session.send("执行异常，请检查权限，参数")
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "flag", 0)
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "info", text)    
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "old_userid", "")
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "userid", "")
            return False