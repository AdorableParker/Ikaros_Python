# import json
# from typing import Optional

# import aiohttp
# from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression
from .AiBot import ai

__plugin_name__ = "图灵AI"
__plugin_usage__ = """------tuling------
关键字："伊卡洛斯"

"我是娱乐用人造天使，α型号「伊卡洛斯」，My Master。"
\t\t\t————伊卡洛斯

########################"""

# 定义无法获取图灵回复时的「表达（Expression）」
EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)


# 注册一个仅内部使用的命令，不需要 aliases
@on_command('tuling', aliases=("伊卡洛斯"))
async def tuling(session: CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = session.state.get('message')
    # 通过封装的函数获取图灵机器人的回复
    # 不调用时默认返回
    # reply = "o_o（伊卡洛斯已经不再能听懂了）"


    # reply = await call_tuling_api(session, message)
    reply = await ai(message)
    if reply:
        await session.finish(reply)
    else:
        pass


@on_natural_language(keywords={""})
async def _(session: NLPSession):
    # 以置信度 60.0 返回 tuling 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候使用 tuling 命令
    return IntentCommand(80.0, 'tuling', args={'message': session.msg_text})




# 弃用第三方ai

#async def call_tuling_api(session: CommandSession, text: str) -> Optional[str]:
#    # 调用图灵机器人的 API 获取回复

#    if not text:
#        return None

#    url = 'http://openapi.tuling123.com/openapi/api/v2'

#    # 构造请求数据
#    payload = {
#        'reqType': 0,
#        'perception': {
#            'inputText': {
#                'text': text
#            }
#        },
#        'userInfo': {
#            'apiKey': session.bot.config.TULING_API_KEY,
#            'userId': context_id(session.ctx, use_hash=True)
#        }
#    }

#    group_unique_id = context_id(session.ctx, mode='group', use_hash=True)
#    if group_unique_id:
#        payload['userInfo']['groupId'] = group_unique_id

#    try:
#        # 使用 aiohttp 库发送最终的请求
#        async with aiohttp.ClientSession() as sess:
#            async with sess.post(url, json=payload) as response:
#                if response.status != 200:
#                    # 如果 HTTP 响应状态码不是 200，说明调用失败
#                    return None

#                resp_payload = json.loads(await response.text())
#                if resp_payload['results']:
#                    for result in resp_payload['results']:
#                        if result['resultType'] == 'text':
#                            # 返回文本类型的回复
#                            return result['values']['text']
#    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
#        # 抛出上面任何异常，说明调用失败
#        return None



#async def call_qingyun_api(session: CommandSession, text: str) -> Optional[str]:
#    # 调用青云机器人的 API 获取回复
#    import requests
#    if not text:
#        return None

#    url = 'http://api.qingyunke.com/api.php?key=free&msg=text{}'.format(text)

#    # 构造请求数据		

# #   response = requests.get(url, params=params)
# #   if not json.loads(response.text)["result"]:
# #       # 返回文本类型的回复
# #       return json.loads(response.text)['content']

#    try:
#        # 使用 aiohttp 库发送最终的请求
#        async with aiohttp.ClientSession() as sess:
#            async with sess.get(url) as response:
#                if response.status != 200:
#                    # 如果 HTTP 响应状态码不是 200，说明调用失败
#                    return None

#                resp_payload = json.loads(await response.text())
#                if not resp_payload['result']:
#                    # 返回文本类型的回复
#                    return resp_payload['content']
#    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
#        # 抛出上面任何异常，说明调用失败
#        return None

