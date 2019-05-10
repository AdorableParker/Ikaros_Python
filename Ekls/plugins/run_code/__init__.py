# -*— coding: utf-8 -*-
from nonebot import on_command, CommandSession

from .get_run_coderesult import get_run_coderesult

__plugin_name__ = "代码运行"
__plugin_usage__ = """------run_code------
命令关键字："run", "运行", "运行代码"
命令输入格式：

运行 代码语言名 代码段

返回：代码运行后返回值

支持语言列表：
c\tgo\tcpp
lua\tphp\tbash
java\tperl\truby
rust\tjulia\tscala
swift\tcsharp\terlang
fsharp\t\tgroovy
kotlin\t\tpython
clojure\t\thaskell
assembly\tjavascript
typescript\tcoffeescript
########################"""


LANGUAGES_LIST = {
    'assembly': 'asm',
    'bash': 'sh',
    'c': 'c',
    'clojure':'clj',
    'coffeescript':'coffe',
    'cpp': 'cpp',
    'csharp': 'cs',
    'erlang': 'erl',
    'fsharp': 'fs',
    'go': 'go',
    'groovy': 'groovy',
    'haskell': 'hs',
    'java': 'java',
    'javascript': 'js',
    'julia': 'jl',
    'kotlin': 'kt',
    'lua': 'lua',
    'perl': 'pl',
    'php': 'php',
    'python': 'py',
    'ruby': 'rb',
    'rust': 'rs',
    'scala': 'scala',
    'swift': 'swift',
    'typescript':'ts',
}


@on_command('run_code', aliases=("run", "运行", "运行代码"), only_to_me=False)
async def run_code(session: CommandSession):
    langunges = session.get('langunges', prompt='运行哪种语言呢？')
    code = session.get('code', prompt='运行的代码是？')
    await session.send('正在运行，请稍等……')
    try:
        langunges = (langunges, LANGUAGES_LIST[langunges])
    except KeyError:
        await session.finish("不支持程序语言 {}\n运行结束".format(langunges))
    output = await get_run_coderesult(langunges, code)
    await session.finish(output + "\n运行结束")

@run_code.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            langunges, *code_list = stripped_arg.split(maxsplit=1)
            if langunges in LANGUAGES_LIST:
                session.state["langunges"] = langunges
            if code_list:
                code = code_list[0].strip()
                if code:
                    session.state['code'] = code
        return

    if not stripped_arg:
        return