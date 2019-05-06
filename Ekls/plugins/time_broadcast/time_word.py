# -*- coding: utf-8 -*-
'''
# 用于提取台词
'''
import os
import time
import random


def get_file_name():
    """
    # 取台词文件列表
    """ 
    address = "{}/plugins/time_broadcast/time_txt/".format(os.getcwd())
    file_info = os.listdir(address)
    fname = random.choice(file_info)
    return address + fname, fname


def line():
    """
    # 取台词内容
    """
    file_dir, file_name, = get_file_name()
    file_text = open(file_dir, encoding='UTF-8')
    i = file_text.readlines()
    localtime = int(time.strftime("%H", time.localtime()))
    i = "{}\n        ——{}".format(i[localtime].strip(), file_name.rstrip(".txt"))
    return i


if __name__ == '__main__':
    print(line())
