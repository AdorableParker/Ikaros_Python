from nonebot import on_command, CommandSession

import requests
import base64
import json


@on_command('trace_moe', aliases=("以图搜番", "搜番"), only_to_me=False)
async def trace_moe (session: CommandSession):
    url = session.get('url', prompt='请提供番剧截图哦')
    # 获取信息
    await session.send("开始搜索咯，稍等哦", at_sender=True)
    success, Fan_drama_info = fan_search(url)
    if success:
        # 向用户发送结果
        await session.send("\n相似度：{0[0]}\n原名：{0[1]}\n中文译名：{0[2]}\n中文别名：{0[3]}\n匹配画面出于第 {0[4]} 番\nAnilist站ID：{0[5]}\nMyanimelist站ID:{0[6]}\n首发时间：{0[7]}\n是否完结：{0[8]}".format(Fan_drama_info), at_sender=True)
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
    response = requests.get(url[0])
    base64_data = base64.b64encode(response.content)
    img_stream = base64_data.decode()
    data = {
        'image': 'data:image/jpeg;base64,{}'.format(img_stream)
        }
    response = requests.post('https://trace.moe/api/search', data=data)
    code = response.status_code
    if code == 400:
        return False, "图片上传失败"
    elif code == 429:
        return False, "请求发送过于频繁，稍后再试\n{}".format(response.text)
    elif code == 500 or code == 503:
        return False, "搜索引擎故障"
    fan_info = json.loads(response.text)["docs"][0]
    similarity = fan_info["similarity"]  # 相似度
    if similarity < 0.87:
        return False, "没有找到可信度达标的结果"
    title_native = fan_info["title_native"]  # 原标题
    title_chinese = fan_info["title_chinese"]  # 中文译名
    synonyms_chinese = fan_info["synonyms_chinese"] # 中文别名
    episode = fan_info["episode"]  # 匹配帧所在番剧集数
    anilist_id = fan_info["anilist_id"] # Anilist站ID
    mal_id = fan_info["mal_id"]# Myanimelist站ID   
    season = fan_info["season"]  # 首发日期
    
    if fan_info["is_adult"]:    # 是否完结
        is_adult = "已完结"
    else:
         is_adult = "连载中"

    return True,(similarity, title_native, title_chinese,
                 synonyms_chinese, episode, anilist_id, 
                 mal_id, season, is_adult)