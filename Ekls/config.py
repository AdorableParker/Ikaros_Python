from nonebot.default_config import *

SUPERUSERS = {1514880969}   # 管理员权限
COMMAND_START = {''}    # 命令前缀符
NICKNAME = {'伊卡洛斯'}   # 昵称
MAX_VALIDATION_FAILURES = 3 # 参数最大错误次数
DEBUG = False   # 调试模式
SESSION_RUNNING_EXPRESSION = "我现在忙着呢，等下再来"   # 已有命令会话运行时回复语
SESSION_CANCEL_EXPRESSION = "命令已取消" # 命令会话取消运行时回复语
TOO_MANY_VALIDATION_FAILURES_EXPRESSION = ('你输错太多次啦，需要的时候再叫我吧', '你输错太多次了，建议先看看使用帮助哦～', '你输错太多次了，使用help命令查看使用帮助哦～')  # 参数错误次数过多时回复语
# 下面参数保持默认-----------------------------------------------
HOST = '127.0.0.1'
PORT = 1234
TULING_API_KEY = 'd146dcf03ae6438d8f53b2e78aafc694'