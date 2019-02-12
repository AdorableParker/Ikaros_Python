# -*— coding: utf-8 -*-
"""
# 搜图 命令
"""

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

import requests
from bs4 import BeautifulSoup
import lxml


@on_command('URL_saucenao', aliases=("链接搜图", "url搜图", "URL搜图"), only_to_me=False)
async def URL_saucenao(session: CommandSession):
    url = session.get('url', prompt='图片链接是什么呢？')
    # 获取信息
    success, img_info = await get_img(url)
    if success:
        # 向用户发送结果
        await session.send("相似度：{0[0]}\n图片名称：{0[1]}\nPixiv ID：{0[2]}\n作品链接：{0[3]}\n画师：{0[4]}\n画师主页：{0[5]}".format(img_info), at_sender=True)
    else:
        await session.send("未找到相似度达标的图片", at_sender=True)

# URL_saucenao.args_parser 装饰器将函数声明为 URL_saucenao 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@URL_saucenao.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['url'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要搜索的图片链接不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


@on_command('img_saucenao', aliases=("图片搜索", "搜图"), only_to_me=False)
async def img_saucenao(session: CommandSession):
    url = session.get('url', prompt='要搜索的图片是哪张呢？')
    # 获取信息
    print(url)
    success, img_info = await get_img(url)
    if success:
        # 向用户发送结果
        await session.send("相似度：{0[0]}\n作品名称：{0[1]}\n作品ID：{0[2]}\n作品链接：{0[3]}\n画师：{0[4]}\n画师主页：{0[5]}".format(img_info), at_sender=True)
    else:
        await session.send(img_info, at_sender=True)


# img_saucenao.args_parser 装饰器将函数声明为 img_saucenao 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@img_saucenao.args_parser
async def _(session: CommandSession):
    # 获取图片url
    stripped_arg = session.current_arg_images
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['url'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('没收到图片哦，再发一次')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


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
    except AttributeError:
        return False, "未找到相似度达标结果"
    except ConnectionError:
        return False, "访问被拒绝，请联系管理员"
    else:
        resul_tsimilarity_info, result_title, pixiv_id, pixiv_id_url, painter, painter_url = '未能获取', '未能获取', '未能获取', '未能获取', '未能获取', '未能获取'
    try:
        # 标题
        result_title = resul_tcontent.select_one("div[class='resulttitle']").get_text()
        # 详情
        details = resul_tcontent.select_one("div[class='resultcontentcolumn']")
        pixiv_id_html, painter_html = details.select("a[class='linkify']")
        # 剥离链接
        pixiv_id_url, painter_url = pixiv_id_html['href'], painter_html['href']
        # 获取信息
        pixiv_id, painter = pixiv_id_html.get_text(), painter_html.get_text()
    except BaseException:
        pass
    # 打包返回
    return True, (resul_tsimilarity_info, result_title, pixiv_id, pixiv_id_url, painter, painter_url)