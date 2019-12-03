from nonebot import on_command, CommandSession
from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.extractors import extract_image_urls
from nonebot.command.argfilter.validators import not_empty
import traceback

from .fan_search import fan_search


__plugin_name__ = "番剧搜索"
__plugin_usage__ = """------trace_moe------
命令关键字："以图搜番", "搜番"
命令输入格式：

以图搜番 <番剧截图>

效果：根据输入的图片，使用trace.moe的引擎进行番剧搜索，返回相似度高于87%的结果中，相似度最高的。

<注意>：由于运算需求过高，请勿频繁调用该命令！

########################"""


@on_command('trace_moe', aliases=("以图搜番", "搜番"), only_to_me=False)
async def trace_moe (session: CommandSession):

    url = session.get(
        'url', prompt='请提供番剧截图哦', 
        arg_filters=[
            handle_cancellation(session), 
            extract_image_urls, 
            not_empty('没收到图片哦，再发一次')
            ]
        )

    # 获取信息
    await session.send("开始搜索咯，稍等哦", at_sender=True)
    try:
        success, Fan_drama_info = await fan_search(url)
    except Exception:
        print("/////////////////////////\n{}\n/////////////////////////".format(traceback.format_exc()))
        await session.send("搜索过程出现问题，错误报告已打印", at_sender=True)
    else:
        if success:
            # 向用户发送结果
            await session.finish("\n相似度：{0[0]:.2%}\n原名：{0[1]}\n中文译名：{0[2]}\n中文别名：{0[3]}\n匹配画面出于第 {0[4]} 番\nAnilist站ID：{0[5]}\nMyanimelist站ID:{0[6]}\n首发时间：{0[7]}\n是否完结：{0[8]}".format(Fan_drama_info), at_sender=True)
        else:
            await session.finish(Fan_drama_info, at_sender=True)


@trace_moe.args_parser
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
