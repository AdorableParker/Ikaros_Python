import nonebot
from nonebot import on_command, CommandSession


__plugin_name__ = "使用说明"
__plugin_usage__ = """
------help------
命令关键字："使用说明", "使用帮助", "帮助", "使用方法"
命令输入格式：

使用帮助 <命令名>

效果：根据输入的命令名，返回帮助信息

########################
"""


@on_command('help', aliases=['使用说明', '使用帮助', '帮助', '使用方法'], only_to_me=False)
async def _(session: CommandSession):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        await session.finish(
            '命令清单：\n\n' + '\n'.join(p.name for p in plugins))
        return

    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if p.name.lower() == arg:
            await session.finish(p.usage)

@on_command('index', aliases=['主页',], only_to_me=False)
async def _(session: CommandSession):
    await session.finish("https://adorableparker.github.io/Hello_World/")