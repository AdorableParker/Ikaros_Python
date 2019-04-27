# -*— coding: utf-8 -*-
"""
# 测试模块
"""

from nonebot import on_command, CommandSession
from nonebot.argparse import ArgumentParser

from .render import render


__plugin_name__ = "翻译"
__plugin_usage__ = """------translation------
命令关键字："翻译"
命令输入格式：

翻译 -o|--original <原文> -t|--to <目标语言>

效果：把原文翻译成目标语种，使用百度翻译api

可翻译语言：
中文\t英语\t文言文\t中文繁体
日语\t韩语\t希腊语\t西班牙语
泰语\t法语\t荷兰语\t阿拉伯语
德语\t俄语\t波兰语\t葡萄牙语
粤语\t丹麦语\t芬兰语\t意大利语
越南语\t捷克语\t瑞典语\t匈牙利语
保加利亚语\t罗马尼亚语
爱沙尼亚语\t斯洛文尼亚语
########################"""


# on_command 装饰器将函数声明为一个命令处理器
@on_command('translation', aliases=("翻译",), only_to_me=False, shell_like=True)
async def translation(session: CommandSession):
    # 向用户发送信息
    parser = ArgumentParser(session=session, usage=__plugin_usage__)
    parser.add_argument('-o', '--original')
    parser.add_argument('-t', '--to')
    args = parser.parse_args(session.argv)
    langlist = {'中文': 'zh', '日语': 'jp', '泰语': 'th', '法语': 'fra', '英语': 'en',
                '西班牙语': 'spa', '韩语': 'kor', '越南语': 'vie', '德语': 'de', '俄语': 'ru',
                '阿拉伯语': 'ara', '爱沙尼亚语': 'est', '保加利亚语': 'bul', '波兰语': 'pl', '丹麦语': 'dan',
                '芬兰语': 'fin', '荷兰语': 'nl', '捷克语': 'cs', '罗马尼亚语': 'rom', '葡萄牙语': 'pt',
                '瑞典语': 'swe', '斯洛文尼亚语': 'slo', '希腊语': 'el', '匈牙利语': 'hu', '意大利语': 'it',
                '粤语': 'yue', '文言文': 'wyw', '中文繁体': 'cht'}
    try:
        text = args.original
        tolanguage = langlist[args.to]
    except:
        echo = "参数不足或不正确，请使用 --help 参数查询使用帮助"
    else:
        echo = render(text, tolanguage)
    await session.finish(echo,at_sender=True)