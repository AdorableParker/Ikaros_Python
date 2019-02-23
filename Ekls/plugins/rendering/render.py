import requests
import hashlib
import urllib
import random
import json


def render(text, toLang = 'zh'):

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
    try:
        out = text["trans_result"][0]["dst"]
    except:
        code = text['error_code']
        if code == '52001':
            out = "error: 请求超时"
        elif code == "52002":
            out = "error: api系统错误"
        elif code == "52003":
            out = "error: 未授权账号"
        elif code == "54000":
            out = "error: 缺少必填参数"
        elif code == "54001":
            out = "error: 安全签名错误"
        elif code == "54003" or code == "54005":
            out = "error: 访问过于频繁"
        elif code == "54004":
            out = "error: 余额不足"
        elif code == "58000":
            out = "error: IP非法"
        elif code == "58001":
            out = "error: 译文不支持"
        elif code == "58002":
            out = "error: 服务已关闭"
    return out
    

if __name__ == '__main__':
    a = "碧蓝航线"
    b = "h"
    print(render(a, b))
