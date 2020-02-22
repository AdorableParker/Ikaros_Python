from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from plugins.rendering import render
import requests
import hashlib
import urllib
import random
import ujson


async def Wisdom(img, zh_content):
    # 获取文案
    jp_content = render(zh_content, "jp").strip().strip("。")
    # 读取素材图片并去色
    img = Image.open(BytesIO(img))
    img = img.convert('L')
    # 获取图片尺寸
    (x, y) = img.size
    # 计算字体字号
    zh_font_size = int(x*0.8/len(zh_content)/1.2)
    jp_font_size = int(x*0.8/len(jp_content)/1.2)
    # 配置字体信息
    zh_font = ImageFont.truetype("font.ttf", zh_font_size)
    jp_font = ImageFont.truetype("font.ttf", jp_font_size)
    # 计算字体绘制位置
    zh_font_xy = (int((x-zh_font_size*len(zh_content))/2), y + int(zh_font_size*0.55))
    jp_font_xy = (int((x-jp_font_size*len(jp_content))/1.8), zh_font_xy[1]+int(zh_font_size*1.1))
    # 计算适合高度
    new_y = int((jp_font_xy[1]+jp_font_size*1.2)*1.05)
    # 绘制图片
    background = Image.new('RGB', (x, new_y), (0, 0, 0))
    background.paste(img, (0, 0))
    # 嵌入文字
    write = ImageDraw.Draw(background)
    write.text(zh_font_xy, zh_content, (255, 0, 0), font=zh_font)
    write.text(jp_font_xy, jp_content, (255, 255, 255), font=jp_font)
    # 转化为数据流
    imgByteArr = BytesIO()
    background.save(imgByteArr, 'jpeg')
    imgBytes = imgByteArr.getvalue() 
    
    # 提交给图床 Air版本
    return imgBytes

    # 转化为Base64并返回 Pro版本
    return base64.b64encode(imgBytes)