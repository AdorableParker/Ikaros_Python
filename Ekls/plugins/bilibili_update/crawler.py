"""
# 爬取B站
"""
import json
import time
import requests
import re


def reto(string, key):
    """
    # 参数(标*为必填参数)：
    # string   待匹配字符串*
    # key    需匹配关键字列表*
    # 返回:
    # 匹配成功返回 Ture
    # 匹配失败返回 False
    """
    rekey = key[0]
    for i in key[1:]:
        rekey = rekey + "|" + i
    out = re.search(rekey, string, flags=0)
    if out is not None:
        return True
    return False


def get_top():
    """
    # 爬取B站排行榜
    """

    params = (
            ('order', 'all'),
    )

    response = requests.get('https://app.bilibili.com/x/v2/rank',
                            params=params, verify=False)
    response.encoding = "UTF-8"
    content = response.text
    text = json.loads(content)["data"]
    echo = []
    for out in text[:3]:
        echo.append({
            "AV": out['param'],
            "播放量": out['play'],
            "评分": out['pts'],
            "标题": out["title"]
         })

    return echo


def get_upper(oid):
    """
    # 更新B站官方动态
    """
    params = (('oid', oid), ('type', "11"))
    response = requests.get('https://api.bilibili.com/x/v2/reply/cursor',
                            params=params, verify=False)
    response.encoding = "UTF-8"
    content = response.text
    text = json.loads(content)
    text = text["data"]["top"]["upper"]["content"]["message"]
    return text


def get_trend(uid, flug=True):
    """
    # 爬取B站动态
    """
    url = 'http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
    response = requests.get(url, params=(('host_uid', uid),))
    response.encoding = "UTF-8"
    content = json.loads(response.text)["data"]["cards"][0]
    uname = content["desc"]['user_profile']["info"]['uname']
    if flug:
        text_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(content["desc"]["timestamp"]))
    else:
        text_time = content["desc"]["timestamp"]
    text = json.loads(content["card"])
    if "item" in text:
        text = text["item"]
        if "description" in text:
            text1 = text["description"]
            img_src = text["pictures"]
            img = "附图:\n"
        else:
            text1 = text["content"]
            img_src = [{"img_src": ""}]
            img = ""

        for img_uil in img_src:
            img = img + img_uil["img_src"] + "\n"

        if reto(text1, ["评论接~", "见评论", "见置顶", "置顶"]):
            oid = content['desc']['rid']
            text1 = text1 + get_upper(oid)

    else:
        text1, img = "专栏标题" + text["title"], ""
    
    return (text1, img, text_time, uname)


async def update2out():
    updata_info = get_trend('233114659')
    # print(updata_info)
    out_info = "{0[0]}\n{0[1]}\n{0[3]} 于 {0[2]} 发布至 哔哩哔哩动态".format(updata_info)
    return out_info

if __name__ == '__main__':
    AX = get_top()
    AXX = get_trend('233114659')
    AXXX = update2out
    print(AXXX)
