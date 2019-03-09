# -*— coding: utf-8 -*-
"""
# 测试模块
"""

from nonebot import permission, on_command, CommandSession
from nonebot.permission import GROUP_ADMIN

__plugin_name__ = "自助禁言"
__plugin_usage__ = """
------banned------
命令关键字："求口", "自助禁言"
命令输入格式：

求口 <时间秒数>

效果：满足你奇怪的要求
########################


"""


# on_command 装饰器将函数声明为一个命令处理器
@on_command('banned', aliases=("求口", "自助禁言"), only_to_me=False)
async def banned(session: CommandSession):
    # 向用户发送信息
    banned_time = session.get('banned_time', prompt='请选择套餐规模\n以分钟为单位')
    bot = session.bot
    try:
        banned_time = int(float(banned_time)*60)
        if banned_time > 2592000:
            banned_time = 2592000
        await bot.set_group_ban(group_id=session.ctx['group_id'],
                                user_id=session.ctx['user_id'],
                                duration=banned_time)
    except:
        pass
        # session.send("执行异常，请检查权限，参数")

@banned.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['banned_time'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的歌曲名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要点播的歌曲），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


# on_command 装饰器将函数声明为一个命令处理器
@on_command('all_banned', aliases=("全员禁言", "全员自闭"),permission=GROUP_ADMIN, only_to_me=False)
async def all_banned(session: CommandSession):
    # 向用户发送信息
    bot = session.bot
    await bot.set_group_whole_ban(group_id=session.ctx['group_id'], enable=True)

# on_command 装饰器将函数声明为一个命令处理器
@on_command('all_not_banned', aliases=("解禁",), only_to_me=False)
async def all_not_banned(session: CommandSession):
    # 向用户发送信息
    bot = session.bot
    await bot.set_group_whole_ban(group_id=session.ctx['group_id'], enable=False)