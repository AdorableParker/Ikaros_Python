import requests
from bs4 import BeautifulSoup

async def get_equipment_list():
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Accept': 'text/css,*/*;q=0.1',
        'Referer': 'http://wiki.joyme.com/blhx/首页',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    response = requests.get('http://wiki.joyme.com/blhx/装备一图榜', headers=headers)
    
    soup = BeautifulSoup(response.text, features="html5lib")
    info = soup.select_one('p[class="info1"]')
    info = info.select('span')
    info = info[2].get_text()
    url = soup.select_one('div[class="noresize"]')
    url = url.select_one("img")
    return url["src"],info


async def get_srength_list():
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'http://wiki.joyme.com/blhx/首页',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    response = requests.post('http://wiki.joyme.com/blhx/PVE用舰船综合性能强度榜', headers=headers)
    soup = BeautifulSoup(response.text, features="html5lib")
    info = soup.select_one('p[class="info1"]')
    info = info.select('span')
    info = info[2].get_text()
    url = soup.select_one('div[class="panel panel-primary"]')
    url = url.select_one("img")
    return url["src"],info


async def get_pixiv_list():
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    response = requests.get('http://wiki.joyme.com/blhx/P站搜索结果一览榜（社保榜）', headers=headers)
    soup = BeautifulSoup(response.text, features="html5lib")
    info = soup.select_one('p[class="info1"]')
    info = info.select('span')
    info = info[2].get_text()
    url = soup.select_one('div[id="mw-content-text"]')
    url = url.select_one("img")
    return url["src"],info