import requests
from bs4 import BeautifulSoup




async def get_and_parse(url):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Length': '0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    url = soup.select_one('div[id="mw-content-text"]').select_one("img")['src']
    updata_date = soup.select_one('li[id="footer-info-lastmod"]').text.replace('本','该')

    return url,updata_date
