# import json
# from typing import Optional

# import aiohttp
# from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression
from .AiBot import ai, training

__plugin_name__ = "图灵AI"
__plugin_usage__ = """------tuling------
关键字："伊卡洛斯"

"我是娱乐用人造天使，α型号「伊卡洛斯」，My Master。"
\t\t\t————伊卡洛斯


$ 多和她聊聊，她会和你的对话中学习如何尬聊

------training_Ai------
命令关键字："教学", "训练", "调教"
命令输入格式：

训练 <问题>#<回答>

$ 伊卡洛斯会完全信任你教给她的所有知识，她把你教给她的所有知识视作珍宝并会很认真的将其牢牢记住..所以请不要让她学坏哦！
$ 关于好感度系统
$ 好感度达到 熟悉 时可以设定一条专属回答
$ 好感度达到 喜欢 时可以设定两条专属回答
$ 好感度达到 爱 时可以设定三条专属回答

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
    if message:
        # reply = await call_tuling_api(session, message)
        reply, rating = await ai(message, session.ctx['user_id'])
        if rating:
            await session.send(reply)
            await session.finish(rating)
        else:
            await session.finish(reply)


@on_natural_language(keywords={""})
async def _(session: NLPSession):
    # 以置信度 60.0 返回 tuling 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候使用 tuling 命令
    return IntentCommand(80.0, 'tuling', args={'message': session.msg_text})



@on_command('training_Ai', aliases=("教学", "训练", "调教"), only_to_me=False)
async def training_Ai(session: CommandSession):
    question = session.get('question', prompt='问题不能为空呢')
    answer = session.get('answer', prompt='想让我回答什么呢')

    report = await training(question, answer,session.ctx['user_id'])
    await session.finish(report)

# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@training_Ai.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            stripped_arg_list = stripped_arg.split("#",1)
            if len(stripped_arg_list) > 1:
                session.state['question'] = stripped_arg_list[0]
                session.state['answer'] = stripped_arg_list[1]
            else:
                session.state['question'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的歌曲名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        if not session.state.get('music_name'):
            session.pause('问题不能为空呢，请重新输入')
        if not session.state.get('music_name'):
            session.pause('想让我回答什么呢，请重新输入')
    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


@on_natural_language(keywords={""})
async def _(session: NLPSession):
    # 以置信度 60.0 返回 tuling 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候使用 tuling 命令
    return IntentCommand(80.0, 'tuling', args={'message': session.msg_text})



@on_command('training_Ai_only', aliases=("只对我说",), only_to_me=False)
async def training_Ai_only(session: CommandSession):
    question = session.get('question', prompt='问题不能为空呢')
    answer = session.get('answer', prompt='想让我回答什么呢')

    report = await training(question, answer, Qid=session.ctx['user_id'], only_to_me=True)
    await session.finish(report)

# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@training_Ai_only.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            stripped_arg_list = stripped_arg.split("#",1)
            if len(stripped_arg_list) > 1:
                session.state['question'] = stripped_arg_list[0]
                session.state['answer'] = stripped_arg_list[1]
            else:
                session.state['question'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的歌曲名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        if not session.state.get('music_name'):
            session.pause('问题不能为空呢，请重新输入')
        if not session.state.get('music_name'):
            session.pause('想让我回答什么呢，请重新输入')
    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg

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

