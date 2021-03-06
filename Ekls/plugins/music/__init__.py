# -*— coding: utf-8 -*-
"""
# 点歌 命令
"""

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .data_source import get_url_of_music



__plugin_name__ = "点歌姬"
__plugin_usage__ = """------music------
命令关键字："点歌", "来首"
命令输入格式：

点歌 <平台>#<歌名>
# 平台默认QQ
效果：根据输入的歌名，使用搜索所指定曲库，返回歌单列表第一条。

########################"""


@on_command('music', aliases=("点歌", "来首"), only_to_me=False)
async def music(session: CommandSession):
    music_name = session.get('music_name', prompt='你想要听哪首歌呢？')
    music_library = session.get('music_library', prompt='请选择平台曲库，目前仅支持：网易云, QQ，默认QQ')
    if music_library in ("网易云","163"):
        music_library = "163"
    else:
        music_library = "qq"
    # 获取歌曲信息
    mysic_report = await get_url_of_music(music_name, music_library)
    # 向用户发送歌曲

    await session.send(mysic_report)
    await session.finish("歌曲消息已发送，若未收到原因类似图片被吞，带来不便还请谅解")


@on_command('post_music_to', aliases=("点歌给",), only_to_me=False)
async def post_music_to(session: CommandSession):
    # 获取歌曲信息
    try:
        music_to = session.ctx["message"][1]["data"]["qq"]
        music_name = session.ctx["message"][2]["data"]["text"]
    except KeyError:
        pass
    else:
        mysic_report = await get_url_of_music(music_name)
        # 向用户发送歌曲
        await session.send("[CQ:at,qq={}],[CQ:at,qq={}]为你送上一首{}".format(music_to,session.ctx["user_id"], music_name))
        await session.finish(mysic_report)
    return 


# music.args_parser 装饰器将函数声明为 music 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@music.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            stripped_arg_list = stripped_arg.split("#",1)
            if len(stripped_arg_list) > 1:
                session.state['music_library'] = stripped_arg_list[0]
                session.state['music_name'] = stripped_arg_list[1]
            else:
                session.state['music_name'] = stripped_arg
                session.state['music_library'] = ""
        return

    if not stripped_arg:
        # 用户没有发送有效的歌曲名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        if not session.state.get('music_name'):
            session.pause('要点播的歌曲名称不能为空呢，请重新输入')
    # 如果当前正在向用户询问更多信息（例如本例中的要点播的歌曲），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


# on_natural_language 装饰器将函数声明为一个自然语言处理器
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(keywords={'点歌给',}, only_to_me=False)
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'post_music_to')