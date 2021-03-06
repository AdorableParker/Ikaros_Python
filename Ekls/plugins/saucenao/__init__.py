# -*— coding: utf-8 -*-
"""
# 搜图 命令
"""

from nonebot import on_command, CommandSession
from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.extractors import extract_image_urls
from nonebot.command.argfilter.validators import not_empty
from .get_img import get_img, ascii2d_api


__plugin_name__ = "图片搜索"
__plugin_usage__ = """------img_saucenao------
命令关键字："图片搜索", "搜图"
命令输入格式：

图片搜索 <图片>

效果：根据输入的图片，使用saucenao搜图引擎进行图源搜索，返回相似度高于60%的结果中，相似度最高的。
########################"""


@on_command('img_saucenao', aliases=("图片搜索", "搜图"), only_to_me=False)
async def img_saucenao(session: CommandSession):

    url = session.get(
        'url', prompt='要搜索的图片是哪张呢？', 
        arg_filters=[
            handle_cancellation(session), 
            extract_image_urls, 
            not_empty('没收到图片哦，再发一次')
            ]
        )

    # 获取信息
    success, img_info = await get_img(url)
    if success:
        # 向用户发送结果
        await session.finish("\n相似度: {info}作品链接: {url[0]}\n画师主页: {url[1]}\n其他相关链接{url[2]}\n预览图: {thumbnail}".format(**img_info), at_sender=True)
    else:
        #info = await ascii2d_api(url)
        info = False
        img_info += """，转用ascii2d引擎搜索
ascii2d引擎搜索结果：
色彩搜索：
最相似来源结果：{0[0]}
作品名：{0[1]}
该作品链接：{0[2]}
作者名：{0[3]}
该作者链接：{0[4]}
预览图：{0[5]}
\n######\n
特征搜索:
最相似来源结果：{1[0]}
作品名：{1[1]}
该作品链接：{1[2]}
作者名：{1[3]}
该作者链接：{1[4]}
预览图：{1[5]}""".format(*info) if info else "\n所有引擎均未成功匹配"
        await session.finish(img_info, at_sender=True)


# img_saucenao.args_parser 装饰器将函数声明为 img_saucenao 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@img_saucenao.args_parser
async def _(session: CommandSession):

    #session.finish("两会期间，该功能关闭的哦")

    # 获取图片url
    stripped_arg = session.current_arg_images
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['url'] = stripped_arg
        return
    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
