import requests
from bs4 import BeautifulSoup
import lxml

from plugins.tool.shorten_url import shorten_url


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
        soup = BeautifulSoup(response.text, "html.parser")
        soup = soup.select_one('div[class="result"]')
        resul_tcontent = soup.select_one('div[class="resultcontent"]')
        # 相似度
        resul_tsimilarity_info = soup.select_one('div[class="resultsimilarityinfo"]').get_text()
        if float(resul_tsimilarity_info.rstrip("%")) < 60:
            return False, "未找到相似度达标结果"
    except AttributeError:
        return False, "未找到相似度达标结果"
    except ConnectionError:
        return False, "访问被拒绝，请联系管理员"
    else:
        result_title, pixiv_id, pixiv_id_url, painter, painter_url = '未能获取', '未能获取', '未能获取', '未能获取', '未能获取'
    try:
        # 标题
        result_title = resul_tcontent.select_one("div[class='resulttitle']").get_text()
    except BaseException:
        pass
    try:
        # 详情
        details = resul_tcontent.select_one("div[class='resultcontentcolumn']")
    except BaseException:
        pass
    try:
        pixiv_id_html, painter_html = details.select("a[class='linkify']")
    except BaseException:
        pass
    try:
        # 剥离链接
        pixiv_id_url, painter_url = shorten_url(pixiv_id_html['href']), shorten_url(painter_html['href'])
    except BaseException:
        pass
    try:
        # 获取信息
        pixiv_id, painter = pixiv_id_html.get_text(), painter_html.get_text()
    except BaseException:
        pass
    # 打包返回
    return True, (resul_tsimilarity_info, result_title, pixiv_id, pixiv_id_url, painter, painter_url)
