from nonebot import on_command, CommandSession
import traceback

from .poem_msxiaobing import writing


__plugin_name__ = "少女诗人小冰"
__plugin_usage__ = """
------poem_bing------
命令关键字："写诗"
命令输入格式：

写诗 <图片素材>

效果：根据输入的图片，让微软小冰创作诗歌。

<注意>：由于运算需求过高，请勿频繁调用该命令！

########################
"""


@on_command('poem_bing', aliases=("写诗",), only_to_me=False)
async def poem_bing (session: CommandSession):
    url = session.get('url', prompt='请提供图片素材哦')
    text = session.get('text')
    # 获取信息
    await session.send("稍等哦，小冰正在酝酿", at_sender=True)
    try:
        verse = await writing(url[0], text)
    except Exception:
        print("/////////////////////////\n{}\n/////////////////////////".format(traceback.format_exc()))
        await session.send("写作过程中出现问题，错误报告已打印", at_sender=True)
    else:
        await session.finish(verse[2])


@poem_bing.args_parser
async def _(session: CommandSession):
    # 获取图片url
    stripped_arg_img = session.current_arg_images
    stripped_arg_text = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg_img:
            session.state['url'] = stripped_arg_img
            if stripped_arg_text:
                session.state['text'] = stripped_arg_text
            else:
                session.state['text'] = ""
        return
    session.state['text'] = ""
    if not stripped_arg_img:
        session.pause('没收到图片哦，再发一次')
    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg_img
