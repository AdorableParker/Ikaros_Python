import requests
import hashlib
import urllib
import random
import json


def render(text, toLang = '中文'):
    langlist = {'中文': 'zh', '日语': 'jp', '泰语': 'th', '法语': 'fra', '英语': 'en',
                '西班牙语': 'spa', '韩语': 'kor', '越南语': 'vie', '德语': 'de', '俄语': 'ru',
                '阿拉伯语': 'ara', '爱沙尼亚语': 'est', '保加利亚语': 'bul', '波兰语': 'pl', '丹麦语': 'dan',
                '芬兰语': 'fin', '荷兰语': 'nl', '捷克语': 'cs', '罗马尼亚语': 'rom', '葡萄牙语': 'pt',
                '瑞典语': 'swe', '斯洛文尼亚语': 'slo', '希腊语': 'el', '匈牙利语': 'hu', '意大利语': 'it',
                '粤语': 'yue', '文言文': 'wyw', '中文繁体': 'cht'}
    toLang = langlist[toLang]
    appid = '20180811000193438'
    secretKey = '3WGh4YP8OYMubp9JOuHa'
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secretKey
    md5 = hashlib.md5()
    md5.update(sign.encode("utf8"))
    sign = md5.hexdigest()
    myurl = ('http://api.fanyi.baidu.com/api/trans/vip/translate?appid={}&q={}&from=auto&to={}&salt={}&sign={}'.format(appid,urllib.parse.quote(text),toLang,str(salt),str(sign)))
        
    r_s = requests.session()
    r = r_s.post(myurl)
    text = json.loads(r.text)
    return text["trans_result"][0]["dst"]
    

if __name__ == '__main__':
    a = "碧蓝航线"
    b = "日语"
    print(render(a, b))
