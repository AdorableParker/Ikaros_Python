from nonebot import on_command, CommandSession
from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.extractors import extract_image_urls
from nonebot.command.argfilter.validators import not_empty

import requests
from bs4 import BeautifulSoup




@on_command('QR_decoding', aliases=("二维码识别","二维码扫描"), only_to_me=False)
async def img_saucenao(session: CommandSession):
    url = session.get(
        'url', prompt='要识别的图片是哪张呢？', 
        arg_filters=[
            handle_cancellation(session),
            extract_image_urls, 
            not_empty('没收到图片哦，再发一次')
            ]
        )
    # 获取信息
    success, info = await QRCode_decoding(url)
    if success:
        await session.finish("识别成功\n{}\n{}\n{}\n{}\n{}".format(*info), at_sender=True)
    else:
        await session.finish(info, at_sender=True)





async def QRCode_decoding(imgurl):
    api, info = "https://zxing.org/w/decode?u=", list()
    print(imgurl)
    response = requests.get(api+imgurl[0])
    soup = BeautifulSoup(response.text, features="lxml")
    title = soup.select_one('title').text
    if title == "Decode Succeeded":
        body = soup.select('tr')
        for i in body:
            info.append(i.select('td')[0].text +":\n"+ i.select('td')[1].text)
        return True, info
    else:
        return False, title