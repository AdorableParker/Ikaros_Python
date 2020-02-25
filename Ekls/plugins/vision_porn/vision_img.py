import requests
import time
import random
import hashlib
import base64
import ujson
from urllib import parse
from config import Tencent_visionporn


async def vision_img(url):
    nonce_str = ''
    for i in range(15):
        nonce_str += random.choice('abcdefghijklmnopqrstuvwxyz0123456789')

    img_base64 = await url2base64(url)
    if not img_base64:
        return '获取图片信息失败'

    data = {
        'app_id': Tencent_visionporn['app_id'],
        'time_stamp': int(time.time()),
        'nonce_str': nonce_str,
        'image': img_base64,
        'app_key': Tencent_visionporn['app_key']
        }

    sign = await get_sign(data)
    data['sign'] = sign
    response = requests.post('https://api.ai.qq.com/fcgi-bin/vision/vision_porn', data=data)
    word = response.text

    dictionary = ujson.loads(word)
    if not dictionary['ret'] == 0:
        return 'Error：{}'.format(dictionary['msg'])
    
    return judge(dictionary['data'])


async def get_sign(data):
    uri_str = ''
    for key in sorted(data.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, parse.quote(str(data[key]), safe = ''))
    sign_str = uri_str + 'app_key=' + data['app_key']

    hash_md5 = hashlib.md5(sign_str.encode('utf-8'))
    return hash_md5.hexdigest().upper()


async def url2base64(url):
    try:
        response = requests.get(url[0])
    except:
        return False
    if response.status_code == 404:
        return False
    return base64.b64encode(response.content).decode()


def judge(data):
    result = {}
    for i in data['tag_list']:
        result[i['tag_name']] = i['tag_confidence']
    
    return '安全度评分：{}\n绅士度评分：{}\n丧尸度评分：{}\n系统综合安全性评分：{}'.format(result['normal'], result['hot'], result['porn'], 100-result['normal_hot_porn'])


# await
#print(vision_img(['https://c2cpicdw.qpic.cn/offpic_new/1514880969//22609e1f-7c62-45d9-82a9-c110ba5dfde2/0?term=2']))