from nonebot.default_config import *

SUPERUSERS = {}   # 超级管理员权限账号
COMMAND_START = {''}    # 命令前缀符
NICKNAME = ('伊卡洛斯')   # 昵称
MAX_VALIDATION_FAILURES = 3 # 参数最大错误次数
DEBUG = False   # 调试模式
# 超出错误次数回复语
TOO_MANY_VALIDATION_FAILURES_EXPRESSION = (
    '你输错太多次啦，需要的时候再叫我吧',
    '你输错太多次了，建议先看看使用帮助哦～',
    '次数超限，本次命令已取消'
)
SESSION_RUNNING_EXPRESSION = "我现在忙着呢，等下再来"   # 已有命令会话运行时回复语
SESSION_CANCEL_EXPRESSION = "命令已取消" # 命令会话取消运行时回复语
#-----------------------------------------------
HOST = '127.0.0.1'
PORT = 1234
# TULING_API_KEY = 'd146dcf03ae6438d8f53b2e78aafc694'
Baidu_fanyi = {"appid" : 'yourAppID',
               "secretKey" : 'yourSecretKey'}

Tencent_visionporn = {'app_id': yourAppID, 
                      'app_key': 'yourAppKey'}

