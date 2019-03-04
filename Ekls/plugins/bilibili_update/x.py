#coding:utf-8
import requests
from bs4 import BeautifulSoup


def get_progress():
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'http://s.360.cn/0kee/a.html?wmode=transparent',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Intervention': '<https://www.chromestatus.com/feature/5718547946799104>; level="warning"',
        'Origin': 'http://wiki.joyme.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Pragma': 'no-cache',
    }
    
    
    response = requests.post('http://wiki.joyme.com/blhx/%E7%A2%A7%E8%93%9D%E6%B5%B7%E4%BA%8B%E5%B1%80%E7%89%B9%E5%88%AB%E6%BC%94%E4%B9%A0%E2%80%A2%E5%9F%83%E5%A1%9E%E5%85%8B%E6%96%AF%E7%BA%A7%E6%B4%BB%E5%8A%A8%E4%B8%93%E9%A2%98', headers=headers)
    
    
    
    soup = BeautifulSoup(response.text, features="html5lib")
    soup = soup.select('table[class="wikitable mw-collapsible"]')[-5:-2]
    info_list = [[],]
    k, q = -1, 0
    for i in soup:
        a = i.select("td")
        for j in a:
            if k == 2:
                info_list.append([])
                q += 1
                k = -1
            k += 1
            info = j.get_text().strip(" ％%\n")
            info_list[q].append(info)

    #print(info_list)
    return info_list

def a(n):
    try:
        output = float(n[1])
    except:
        output = 100.0
    return output

def get_ing():
    info_list = get_progress()
    out = "下表依进度排名\n服务器名\t进度\t更新时间"
    info_list = sorted(info_list, key=a, reverse=False)
    for i in info_list:
        out += "\n{0[0]}\n{0[1]}%\t{0[2]:　>10s}".format(i)
    return out
#print(get_ing())