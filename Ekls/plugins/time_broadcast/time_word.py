# -*- coding: utf-8 -*-
'''
# 用于提取台词
'''
import os
import time
import random


def file_name():
    """
    # 取台词文件列表
    """ 
    address = "{}/plugins/time_broadcast/time_txt/".format(os.getcwd())
    file_info = os.listdir(address)
    return address + random.choice(file_info)


def line():
    """
    # 取台词内容
    """
    fname = file_name()
    file_text = open(fname, encoding='UTF-8')
    i = file_text.readlines()
    localtime = int(time.strftime("%H", time.localtime()))
    i = i[localtime].strip()
    return i


if __name__ == '__main__':
    print(line())
