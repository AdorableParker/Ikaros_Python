from typing import Optional


from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from config import NICKNAME

from plugins.tool.date_box import sql_rewrite, sql_read, sql_write, sql_delete


__plugin_name__ = "复读姬"
__plugin_usage__ = """------repeat------

人类的本质是什么？

给我把倒数第二个复读机砸了！
########################
#
# 欲启用此功能请使用命令： 控制台"""


# 注册一个仅内部使用的命令，不需要 aliases
@on_command('repeat')
async def repeat(session: CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = session.state.get('message')
    await get_repeat(session, message)


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    # 以置信度 60.0 返回 tuling 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候触发命令

    return IntentCommand(60.0, 'repeat', args={'message': session.msg_text})

async def get_repeat(session: CommandSession, text: str) -> Optional[str]:
    # 查询数据库
    if not text:
        return None
    switch = sql_read("User.db", "group_info", "group_id", session.ctx["group_id"], field = "repeat", in_where = True)  # 权限管理器
    if not switch:  # 如果没有这个群的配置记录，则添加一条，默认全部为False
       sql_write("User.db", "group_info (id, group_id)",'(Null, {})'.format(session.ctx["group_id"]))
    elif not switch[0][0]:  # 如果配置记录为关闭，则退出
        pass
    else:
        try:
            old_info, flag, user, old_user = sql_read("User.db", "repeat_info", "groupid", session.ctx["group_id"])[0][:4]
        except IndexError:
            # 初步判定为未添加复读
            sql_write("User.db", "repeat_info",'("", 0, Null, Null,{})'.format(session.ctx["group_id"]))
        else:
            if old_info == text:
                if flag > 1 or flag == 0:
                    text = False
                flag += 1
                # 更改数据库
                sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "flag", flag)  # 复读次数
                sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "old_userid", user)  # 更迭在位者id
                sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "userid", session.ctx["user_id"])  # 记录继位者id
                await session.finish(text)
            else:
                if flag >= 2 and False:
                    bot = session.bot
                    try:
                        # 禁言在位者
                        await bot.set_group_ban(group_id=session.ctx['group_id'], 
                                                user_id=old_user,
                                                duration=flag*120)
                        if old_user != session.ctx['user_id']:  #判断是否自己打断自己
                            # 禁言篡位者
                            await bot.set_group_ban(group_id=session.ctx['group_id'], 
                                                    user_id=session.ctx['user_id'],
                                                    duration=flag*100)
                    except:
                        await session.send("执行异常，请检查权限，参数")
                # 更改数据库
                sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "flag", 0)  # 清空次数
                sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "info", text)  # 更新文本
                sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "old_userid", "")  # 清空在位者id
                sql_rewrite("User.db", "repeat_info", "groupid", session.ctx["group_id"], "userid", "")  # 清空继位者id
    return None
