from nonebot import on_command, CommandSession
from nonebot.command.argfilter.extractors import extract_text
from nonebot.command.argfilter.validators import match_regex
from nonebot.command.argfilter.controllers import handle_cancellation
from .startshipbuilding import startshipbuilding
__plugin_name__ = "碧蓝建造模拟器"
__plugin_usage__ = """------MurphyisLaw------
命令关键字："建造模拟", "模拟建造"
命令输入格式：
建造模拟 <类型> [次数] 
$ 类型参数选填
    
    轻/轻型/a/A/1
    重/重型/b/B/2
    特/特型/c/C/3

#######################"""

TYPE = {"轻型":("轻", "轻型", "a", "A", "1"), 
        "重型":("重", "重型", "b", "B", "2"), 
        "特型":("特", "特型", "c", "C", "3")}


@on_command("MurphyisLaw", aliases=("建造模拟", "模拟建造"), only_to_me=False)
async def MurphyisLaw (session: CommandSession):
    buildnum = session.get_optional('num',default=1)
    buildtype = session.get('type', prompt='要建造哪个类型呢？', 
                            arg_filters=[
                                match_regex(pattern=r'轻|轻型|重|重型|特|特型|[a-cA-C1-3]', message='格式不正确，请重输', fullmatch=True),
                                handle_cancellation(session), 
                            ])
    for i in TYPE:
        if buildtype in TYPE[i]:
            buildresult = await startshipbuilding(i, buildnum)

    await session.finish("\n建造类型：{}\n建造次数：{}\n{}".format(buildtype, buildnum, buildresult), at_sender=True)




@MurphyisLaw.args_parser
async def _(session: CommandSession):

    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        stripped_arg = stripped_arg.split(" ",1)
        for i in TYPE:
            if stripped_arg[0] in TYPE[i]:
                session.state['type'] = i
                break
        else:
            await session.send('格式不正确，请重输')
        if len(stripped_arg) >= 2:
            session.state['num'] = stripped_arg[1]
        else:
            session.state['num'] = 1
    return