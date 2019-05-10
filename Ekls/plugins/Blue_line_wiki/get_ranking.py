import requests
from bs4 import BeautifulSoup

async def get_equipment_list():
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Accept': 'text/css,*/*;q=0.1',
        'Referer': 'http://wiki.joyme.com/blhx/%E9%A6%96%E9%A1%B5',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    response = requests.get('http://wiki.joyme.com/blhx/%E8%A3%85%E5%A4%87%E4%B8%80%E5%9B%BE%E6%A6%9C', headers=headers)
    
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
        'Referer': 'http://wiki.joyme.com/blhx/%E9%A6%96%E9%A1%B5',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    response = requests.post('http://wiki.joyme.com/blhx/PVE%E7%94%A8%E8%88%B0%E8%88%B9%E7%BB%BC%E5%90%88%E6%80%A7%E8%83%BD%E5%BC%BA%E5%BA%A6%E6%A6%9C', headers=headers)
    soup = BeautifulSoup(response.text, features="html5lib")
    info = soup.select_one('p[class="info1"]')
    info = info.select('span')
    info = info[2].get_text()
    url = soup.select_one('div[class="panel panel-primary"]')
    url = url.select_one("img")
    return url["src"],info