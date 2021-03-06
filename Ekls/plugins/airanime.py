import nonebot
from nonebot import on_command, CommandSession

import requests
import ujson

from plugins.tool import shorten_url

__plugin_name__ = "搜番源"
__plugin_usage__ = """------air_nime------
命令关键字："搜动漫", "搜索动漫", "动漫资源", "动漫搜索", "搜索番剧", "番剧资源", "番剧搜索"
命令输入格式：

番剧搜索 <番剧名>

效果：根据输入的番剧名，返回搜索到的番剧资源链接

别想了，没有里番的(〜￣△￣)〜
感谢 Trii Hsia 提供服务
########################"""


@on_command('air_nime', aliases=['搜番源', '搜动漫', '搜索动漫', '动漫资源', '动漫搜索', '搜索番剧', '番剧资源', '番剧搜索'], only_to_me=False)
async def _(session: CommandSession):

    #session.finish("两会期间，该功能关闭的哦")

    arg = session.current_arg_text.strip().lower()
    if not arg:
        # 如果用户没有发送参数，则发送提示信息
        await session.finish("需要搜索的番名不能为空哦")
        return
    await session.send('正在搜索，稍等哦')
    airanime_api = 'http://airanime.applinzi.com/function/sonline.php?kt={}'.format(arg)
    response = requests.get(airanime_api)
    if not response.ok:
        await session.finish('搜索失败了，请稍后再试吧')
        return
    try:
        result_dic = ujson.loads(response.text)
    except:
        await session.finish('服务提供商出现问题')
    sites =[
        ('bilibili', '哔哩哔哩'),
        ('dilidili', '嘀哩嘀哩'),
        ('anime1', 'Anime1'),
        ('calibur', 'Calibur'),
        ('qinmei', 'Qinmei'),
        ('iqiyi', '爱奇艺'),
        ('tencenttv', '腾讯视频'),
        ('fcdm', '风车动漫'),
        ('youku', '优酷'),
        # ('pptv', 'PPTV'),
        ('letv', '乐视'),
        ]
    output = "来源：\n"
    for key, source_name in sites:
        name_list, url_list, number_of_sources = result_dic[key]
        if number_of_sources:
            output += source_name + ":\n"
            for i in range(number_of_sources):
                short_link = shorten_url.shorten_url(url_list[i])
                output += " \t{}:{}\n".format(name_list[i], short_link)
    await session.finish(output)
