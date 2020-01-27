from sql import database
import requests
from bs4 import BeautifulSoup


headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Length': '0'
}

response = requests.get('https://wiki.biligame.com/blhx/重樱船名称对照表', headers=headers)
soup = BeautifulSoup(response.text, features="lxml")
soup = soup.select_one('table[id="FlourPackage"]')
soup_list = soup.select('tr[class="Flour"]')

db = database('User')

code_list = list(map(lambda x: x[0], db.select('Roster')))
name_list = list(map(lambda x: x[1], db.select('Roster')))
print(code_list)
print(name_list)
z = 1
for i in soup_list:
    z +=1
    #print("{}/{}".format(z, len(soup_list)),end="\r")
    j = i.select_one("span[lang='zh']").text
    k = i.select_one('span[class="nowrap"]')
    if not k:
        k = i.select_one('span[class="new nowrap"]')
    k = k.text
    if j in code_list:
        if k != name_list[code_list.index(j)]:
            print(j,k)
            db.updata('Roster', condition="name = '{}'".format(k), code="'{}'".format(j))
    else:
        print(j,k)
        db.insert_into('Roster', code=j, name=k)

db.close_database()

'''

name_list = list(db.select('ship_map', output_field=('Usedname',)))
for i in name_list:
    if "(" not in i[0]:
        new_name = "'{}(N/白)'".format(i[0])
        db.updata('ship_map', condition="Usedname = '{}'".format(i[0]), Usedname=new_name)

name_list = db.select('ship_map', output_field=('Usedname',))
for i in name_list:
    if "(" not in i[0]:
        print(i[0])
db.close_database()
'''
