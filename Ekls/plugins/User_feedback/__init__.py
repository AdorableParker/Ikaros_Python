from nonebot import on_command, CommandSession
from .submit_feedback import submit_feedback

__plugin_name__ = "用户反馈"
__plugin_usage__ = """------feedback------
命令关键字："用户反馈", "反馈", "异常反馈"
命令输入格式：

反馈 <需要反馈内容>

每条反馈开发者都会查看，但是时间不一定

相关使用问题建议请 活用搜索引擎 并且 自助使用help命令查看帮助信息

使用中出现异常 亦或是 脑洞、有意思的需求、想法 欢迎提出

为了尽快的修复可能的bug 或是 改善使用中不便的地方
请尽量 具体详细描述问题出现前后所做事项，以便于重现问题

开发者欢迎 聪明的问题 且讨厌 愚蠢的提问
例如：
聪明的提问：当我发送命令点歌 "网易云#Fallen Down" 时，没有正常的发送歌曲分享链接，并且没有任何反馈。

愚蠢的问题：点歌功能怎么用

如果对于提问的艺术有兴趣，可以参考
《提问的智慧》http://git.io/how2ask
相信我，学会提问这将让你受益良多

另外如果希望提供有趣的想法，或是希望添加某些需求
这很欢迎，但请注意：
If the implementation is hard to explain, it's a bad idea.
如果 这个 想法 是 难以 解释，它是 一个 坏 主意
If the implementation is easy to explain, it may be a good idea.
如果 这个 想法 是 容易 解释，它是 一个 好 点子

请尽量准确清晰的描述你的想法或需求
并且开发将将有可能直接联系你以询问更多细节

开发者 最后编写于
2019年4月27日
########################"""


@on_command('feedback', aliases=("用户反馈", "反馈", "异常反馈"), only_to_me=False)
async def feedback(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if not stripped_arg:
            await session.pause("欢迎您的反馈，建议先通过 help命令 阅读反馈命令说明。\n现在已经进入反馈录入模式，您接下来的文字信息将会被上传至数据库\n输入“取消反馈”将退出反馈录入并结束此次对话", at_sender = True)
        else:
            await submit_feedback(stripped_arg, session.ctx["user_id"])
            await session.finish("反馈已经提交，感谢您的支持", at_sender = True)
    elif not stripped_arg:
        session.pause('空值不予录入哦，请输入需反馈信息\n输入“取消反馈”将退出反馈录入并结束此次对话')
    elif stripped_arg == "取消反馈":
        await session.finish("已退出反馈录入模式", at_sender = True)
    else:
        await submit_feedback(stripped_arg, session.ctx["user_id"])
        await session.finish("反馈已经提交，感谢您的支持", at_sender = True)