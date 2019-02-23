from nonebot import CommandGroup

__plugin_name__ = 'B站番剧指南'
__plugin_usage__ = """
------banned------
关键字："番", "动漫", "动画"【需要at】

触发示例：

最近有什么新番
18年7月有啥动漫
约会大作战什么时候更新
梦幻岛今天更新了吗
刀剑神域明天会更新嘛

########################
"""

cg = CommandGroup('anime_index')

from . import index, timeline, nlp