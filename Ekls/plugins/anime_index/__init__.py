from nonebot import CommandGroup

__plugin_name__ = 'anime_index'

cg = CommandGroup('anime_index')

from . import index, timeline, nlp