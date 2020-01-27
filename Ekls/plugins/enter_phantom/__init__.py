from nonebot import on_command, CommandSession
from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.extractors import extract_image_urls, extract_text
from nonebot.command.argfilter.validators import not_empty
from .phantom import getimg, phantom, up_img
from .Wisdom import Wisdom

__plugin_name__ = "幻影坦克图片制作"
__plugin_usage__ = """------enter_phantom------
命令关键字：幻影坦克制作

效果：输入需要制作的两张图片，返回制作完成的图片的下载链接

<注意>：由于运算需求极高，请勿频繁调用该命令！

Everything is a phantom

$ 原理在这里：
$ https://www.bilibili.com/video/av75403051/
$ 看看能不能带动一波播放量2333


------this_is_wisdom------
命令关键字：注入至理

效果：输入需要图片素材以及文案，返回制作完成的图片的下载链接

<注意>：由于堵塞式上载图床，完成的图片上传时会短暂卡顿

A famous saying whose essence is truth itself;

########################"""


@on_command('enter_phantom', aliases=("幻影坦克制作",), only_to_me=False)
async def enter_phantom(session: CommandSession):

    url_A = session.get(
        'url_A', prompt='请提供第一张图片', 
        arg_filters=[
            handle_cancellation(session), 
            extract_image_urls, 
            not_empty('没收到图片哦，再发一次')
            ]
        )
    url_B = session.get(
        'url_B', prompt='请提供第二张图片', 
        arg_filters=[
            handle_cancellation(session), 
            extract_image_urls, 
            not_empty('没收到图片哦，再发一次')
            ]
        )
    await session.send("开始生成咯，稍等呢", at_sender=True)
    # 获取信息
    img_A, img_B = await getimg(url_A[0]), await getimg(url_B[0])
    if img_A and img_B:
        photo = await phantom(img_A, img_B)
        info = await up_img(photo)
    else:
        info = "图片下载失败"
    await session.finish(info, at_sender=True)


@on_command("this_is_wisdom", aliases=("注入至理",), only_to_me=False)
async def this_is_wisdom (session: CommandSession):
    url = session.get('url', prompt='请提供图片素材哦',
        arg_filters=[
            handle_cancellation(session), 
            extract_image_urls, 
            not_empty('没收到图片哦，再发一次')
            ]
        )
    text = session.get('text', prompt='请输入文案文本', 
        arg_filters=[
            handle_cancellation(session), 
            extract_text, 
            not_empty('没收到文案哦，再发一次')
            ])
    # 获取信息
    await session.send("稍等哦，正在生成", at_sender=True)
    img = await getimg(url[0])
    if img:
        photo = await Wisdom(img, text)
        info = await up_img(photo)
    else:
        info = "图片下载失败"
    await session.finish(info, at_sender=True)
