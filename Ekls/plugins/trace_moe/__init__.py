from nonebot import on_command, CommandSession

import requests
import base64



@on_command('trace_moe', aliases=("以图搜番", "搜番"), only_to_me=False)
async def trace_moe (session: CommandSession):
    url = session.get('url', prompt='请提供番剧截图哦')
    # 获取信息
    await session.send("开始搜索咯，稍等哦", at_sender=True)
    success, Fan_drama_info = await fan_search(url)
    if success:
        # 向用户发送结果
        await session.send("相似度：{0[0]}\n作品名称：{0[1]}\n作品ID：{0[2]}\n作品链接：{0[3]}\n画师：{0[4]}\n画师主页：{0[5]}".format(Fan_drama_info), at_sender=True)
    else:
        await session.send(Fan_drama_info, at_sender=True)


@trace_moe.args_parser
async def _(session: CommandSession):
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


def fan_search(url):
    response = requests.get(url)
    base64_data = base64.b64encode(response.content)
    img_stream = base64_data.decode()
    data = {
        'image': 'data:image/jpeg;base64,{}'.format(img_stream)
        }
    response = requests.post('https://trace.moe/api/search', headers=headers, data=data)
    print(response.text)
    return False, "测试中……"