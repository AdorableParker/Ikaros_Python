import requests
from bs4 import BeautifulSoup


async def get_img(url):
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;",
        "Accept-Encoding":"gzip",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Referer":"https://saucenao.com/",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
    params = (
        ('db', '999'),
        ('url', url),
        )
    try:
        response = requests.get('https://saucenao.com/search.php', headers=headers, params=params)
        root_soup = BeautifulSoup(response.text, features="lxml")
        soup = root_soup.select_one('div[class="result"]')

        resultmiscinfo = soup.select_one('div[class="resultmiscinfo"]') # 尝试获取关联链接
        related_links = resultmiscinfo.find_all("a")

        resul_tcontent = soup.select_one('div[class="resultcontent"]')
        list_info = resul_tcontent.select("div")[0]
    except AttributeError:
        return False, "未找到相似度达标结果"
    except ConnectionError:
        return False, "\nConnectionError\n连接错误\n访问被拒绝，请联系管理员"
    
    j = [text for text in soup.stripped_strings]
    if float(j[0].rstrip("%")) < 60:
        return False, "saucenao引擎未找到相似度大于60的结果"
    else:
        # 缩略图
        thumbnail_img = root_soup.select_one('div[class="resultimage"]')
        try:
            thumbnail_url = thumbnail_img.img["data-src"]
        except KeyError:
            thumbnail_url = thumbnail_img.img["src"]

        # 信息
        out_info = j[0] + "\n"
        for i in j[1:]:
            if not i.endswith(":"):
                out_info += "{}\n".format(i)
            else:
                out_info += "{}  ".format(i)

    #尝试获取Pixiv链接
    try:
        # 剥离链接
        details = resul_tcontent.select_one("div[class='resultcontentcolumn']")
        url_list = []
        for i in details.select("a[class='linkify']"):
            url_list.append(i["href"])
        if not url_list:
            url_list = ["-", "-"]
        else:
            url_list.append("-")
        url_list.append("")
    except BaseException:
        pass
    for i in related_links:
        url_list[2] += i["href"] + "\n"

    # 打包返回
    return True, {"info":out_info, "url":url_list, "thumbnail":thumbnail_url}


async def ascii2d_api(img_url):
    url = 'https://ascii2d.net/search/url/{}'.format(img_url[0])
    headers = {
        'authority': 'ascii2d.net',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    }

    response = requests.get(url, headers=headers)
    response = requests.get(response.url, headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    soup = soup.select('div[class="row item-box"]')
    soup_list = map(lambda xx : xx.select('h6 > img'), soup)
    for i in soup_list:
        if i:
            in_from = i[0]['alt']
            aims = i[0].next_sibling.next_sibling
            writer = aims.next_sibling.next_sibling
            aims_url = aims['href']
            aims_name = aims.text
            writer_url = writer['href']
            writer_name = writer.text
            return (in_from, aims_name, aims_url, writer_name, writer_url)