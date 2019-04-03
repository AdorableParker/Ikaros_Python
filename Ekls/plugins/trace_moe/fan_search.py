import requests
import base64
import json


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
        return False, "搜索引擎故障，请不要使用动态图片"
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
        is_adult = "连载中"
    else:
         is_adult = "已完结"

    return True,(similarity, title_native, title_chinese,
                 synonyms_chinese, episode, anilist_id, 
                 mal_id, season, is_adult)
