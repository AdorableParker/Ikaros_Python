"""
# 点歌 处理
"""

import json
import requests

from aiocqhttp.message import MessageSegment

async def get_url_of_music(music_name: str) -> str:
    # 这里返回歌曲数据
    text = inquire(music_name)
    if text["code"] == 200:
        while "msg" in text:
            music_name = music_name[0:len(music_name)-1]
            text = inquire(music_name)
        try:
            number_of_results = text["result"]["songCount"]
        except TypeError:
            return "网易云拒绝服务"
        else:
            if number_of_results != 0:
                uid = str(text["result"]["songs"][0]["id"])
                return "[CQ:music,type=163,id={}]".format(uid)
            else:
                return "没有名叫{}的歌曲".format(music_name)
    elif text["code"] == 400:
        return "网易云拒绝访问"
    else:
        return "网络异常"
        

def get_music(content):
    """
    # 获取歌曲信息
    # 歌曲信息排版
    """
    text = inquire(content)
    if text["code"] == 200:
        while "msg" in text:
            content = content[0:len(content)-1]
            # print (content)
            text = inquire(content)
        if text["result"]["songCount"] != 0:
            uid = str(text["result"]["songs"][0]["id"])
            aid = text["result"]["songs"][0]["name"]
            artistname = text["result"]["songs"][0]["artists"][0]["name"]
            qed = [
                "http://music.163.com/outchain/player?type=2&id="+ uid,
                "http://music.163.com/song/media/outer/url?id="+ uid +".mp3",
                aid,
                artistname,
                'https://s4.music.126.net/style/web2/img/default/default_album.jpg',
                200]
        else:
            qed = ["没有名叫"+content+"的歌曲", "", "", "", 404]
    elif text["code"] == 400:
        qed = ["查询出错\nError-400", "", "", 400]
    else:
        qed = ["Error", "", "", 500]
    return qed


def inquire(musuc_name):
    """
    # 搜索网易云
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    }

    params = (
        ('csrf_token', 'hlpretag='),
        ('hlposttag', ''),
        ('s', musuc_name),
        ('type', '1'),
        ('offset', '0'),
        ('total', 'true'),
        ('limit', '1'),
    )

    result = requests.get('http://music.163.com/api/search/get/web', headers=headers, params=params)
    return json.loads(result.text)


if __name__ == '__main__':
    #print(get_music(input()))
    print(inquire("激昂壮志"))