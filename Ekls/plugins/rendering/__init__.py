# -*— coding: utf-8 -*-
"""
# 测试模块
"""

from nonebot import on_command, CommandSession
from .render import render

__plugin_name__ = "翻译"
__plugin_usage__ = """
------translation------
命令关键字："翻译"
命令输入格式：

翻译 <原文>

效果：把原文翻译成目标语种，使用百度翻译api

可翻译语言：
中文\t英语\t文言文\t繁体中文
日语\t韩语\t希腊语\t西班牙语
泰语\t法语\t荷兰语\t阿拉伯语
德语\t俄语\t波兰语\t葡萄牙语
粤语\t丹麦语\t芬兰语\t意大利语
越南语\t捷克语\t瑞典语\t匈牙利语
保加利亚语\t罗马尼亚语
爱沙尼亚语\t斯洛文尼亚语
########################
"""


# on_command 装饰器将函数声明为一个命令处理器
@on_command('translation', aliases=("翻译",), only_to_me=False)
async def translation(session: CommandSession):
    # 向用户发送信息
    text = session.get('text', prompt='要翻译哪句话呢')
    tolanguage = session.get('tolanguage', prompt='请选择目标语言')
    echo = render(text, tolanguage)
    await session.send(echo,at_sender=True)


@translation.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['text'] = stripped_arg
        return

    if not stripped_arg:
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('请重新输入')

    session.state[session.current_key] = stripped_arg
