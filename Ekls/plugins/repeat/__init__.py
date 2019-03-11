import json
from typing import Optional


from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand


from plugins.tool.data_box import sql_rewrite, sql_read


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
        await session.finish(escape(reply))


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
            if flag > 1 or flag == 0:
                text = False
            flag += 1
            # 写入数据库
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "flag", flag)  # 复读次数
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "old_userid", user)  # 更迭在位者id
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "userid", session.ctx["user_id"])  # 记录继位者id
            return text
        else:
            if flag >= 2:
                bot = session.bot
                try:
                    # 禁言在位者
                    await bot.set_group_ban(group_id=session.ctx['group_id'], 
                                            user_id=old_user,
                                            duration=flag*120)
                    # 禁言篡位者
                    await bot.set_group_ban(group_id=session.ctx['group_id'], 
                                            user_id=session.ctx['user_id'],
                                            duration=flag*100)
                except:
                    await session.send("执行异常，请检查权限，参数")
            # 写入数据库
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "flag", 0)  # 清空次数
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "info", text)  # 更新文本
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "old_userid", "")  # 清空在位者id
            sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "userid", "")  # 清空继位者id
            return False