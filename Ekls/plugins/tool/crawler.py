"""
# 爬取B站
"""
import json
import time
import requests
import re

from plugins.tool import shorten_url

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
    # 判断更新B站官方动态
    """
    params = (('oid', oid), ('type', "11"))
    response = requests.get('http://api.bilibili.com/x/v2/reply/cursor',
                            params=params, verify=False)
    response.encoding = "UTF-8"
    content = response.text
    #print(content)
    text = json.loads(content)
    text = text["data"]["top"]["upper"]
    return text


def get_trend_getweb(uid):
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
    response = requests.get(url, params=(('host_uid', uid),))
    response.encoding = "UTF-8"
    return response

def get_trend(uid, cards:int=0, flag=True):
    """
    # 爬取B站动态
    # 针对碧蓝航线的动态进行了内容处理
    """
    for _ in range(3):
        response = get_trend_getweb(uid)
        if not json.loads(response.text)["code"]:
            inform_content = {"code":0}
            break
    else:
        inform_content = {"code":1}
        return 
    content = json.loads(response.text)["data"]["cards"][cards]
    try:
        sign_info = content["desc"]['user_profile']["info"]
        inform_content["sign"] = sign_info.get('uname',"")
    except:
        print("////////////////////////////////////////////")
        print(content)
        print("////////////////////////////////////////////")
    if flag:
        inform_content["posted_time"] = time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(content["desc"]["timestamp"]))
    else:
        inform_content["posted_time"] = content["desc"]["timestamp"]

    text = json.loads(content["card"])
    if "item" in text:
        text = text["item"]
        if "description" in text:
            text1 = text["description"]
            img_src = text.get("pictures", False)
            if not img_src:
                img_src = [{"img_src":text.get("cover").get("default","")}] # 获取小视频封面
            img = "附图:\n"
            for img_uil in img_src:
                img_suil = shorten_url.shorten_url(img_uil["img_src"])
                img += img_suil + "\n"
            inform_content["img"] = img
        else:
            text1 = text["content"]

        if reto(text1, ["评论接", "见评论", "见置顶", "置顶"]):
            oid = content['desc']['rid']
            supplement = get_upper(oid)
            text1 += "\n\n{}".format(supplement["content"]["message"])
            supplement_add = {}
            for add_to in supplement["replies"]:
                if add_to["mid"] == int(uid):
                    supplement_add[add_to['ctime']] = add_to["content"]["message"]
            for ctime in sorted(supplement_add):
                text1 += "\n\n{}".format(supplement_add[ctime])
        inform_content["main_body"] = text1
        
    else:
        inform_content["main_body"] = "专栏标题:{}\n专栏摘要：\n{}…".format(text["title"],text.get("summary",""))
    return inform_content


async def update2out(uid, cards=0):
    updata_info = get_trend(uid, cards)
    # print(updata_info)
    img_url = updata_info.get("img","")
    main_body = updata_info.get("main_body","")
    sign = updata_info.get("sign", "")
    text_time = updata_info["posted_time"]
    out_info = "{}\n{}\n{} 于 {} 发布至 BiliBili 动态".format(main_body, img_url, sign, text_time)
    return out_info

if __name__ == '__main__':
    #AX = get_top()
    #AXX = get_trend('300123440')
    AXX = get_trend("233114659")
    print(AXX)
