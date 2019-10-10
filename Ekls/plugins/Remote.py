from nonebot import on_command, CommandSession
from nonebot.permission import SUPERUSER
from os import system


@on_command('remote', aliases=['启动远程',], only_to_me=False, permission=SUPERUSER)
async def _(session: CommandSession):
    system("TeamViewer.exe")
    await session.finish("命令已执行")