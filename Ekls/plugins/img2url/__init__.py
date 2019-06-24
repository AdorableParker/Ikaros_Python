from nonebot import on_command, CommandSession, get_bot
from plugins.tool import shorten_url


__plugin_name__ = "图片转地址"
__plugin_usage__ = """------retelling------
命令关键字："地址化", "img2url"
命令输入格式：

地址化 <图片>

效果：返回地址化后的短链接

########################"""


@on_command('img2url', aliases=("地址化",), only_to_me=False)
async def img2url(session: CommandSession):

    [img_url] = session.get('url', prompt='要搜索的图片是哪张呢？')
    await session.finish(shorten_url.shorten_url(img_url), at_sender=True)


@img2url.args_parser
async def _(session: CommandSession):

    #session.finish("两会期间，该功能关闭的哦")

    # 获取图片url
    stripped_arg = session.current_arg_images
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['url'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('没收到图片哦，再发一次')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
