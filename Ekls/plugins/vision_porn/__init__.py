# -*— coding: utf-8 -*-
"""
# 搜图 命令
"""

from nonebot import on_command, CommandSession
from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.extractors import extract_image_urls
from nonebot.command.argfilter.validators import not_empty
from .vision_img import vision_img


__plugin_name__ = "图片鉴黄"
__plugin_usage__ = """------vision_porn------
命令关键字："图片鉴黄", "鉴黄"
命令输入格式：

图片鉴黄 <图片>

效果：根据输入的图片，使用腾讯图片鉴黄接口进行色情鉴定，返回鉴定结果文档。
########################"""


@on_command('img_saucenao', aliases=("图片鉴黄", "鉴黄"), only_to_me=False)
async def img_saucenao(session: CommandSession):

    url = session.get(
        'url', prompt='要鉴定的图片是哪张呢？', 
        arg_filters=[
            handle_cancellation(session), 
            extract_image_urls, 
            not_empty('没收到图片哦，再发一次')
            ]
        )

    # 获取信息
    comment = await vision_img(url)
    await session.finish(comment, at_sender=True)


# img_saucenao.args_parser 装饰器将函数声明为 img_saucenao 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@img_saucenao.args_parser
async def _(session: CommandSession):

    # 获取图片url
    stripped_arg = session.current_arg_images
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['url'] = stripped_arg
        return
    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
