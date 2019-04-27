# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 22:20:59 2018

@author: Administrator
"""
import time
import math
import configparser



def typesetting(gap, progress):
    """
    # 排版
    """
    time_gap = int(gap // 86400)
    if time_gap < 0:
        text_gap = "活动已经结束了呢"
        change_configuration()
    elif not time_gap:
        time_gap = int(gap // 3600)
        print(gap)
        text_gap = "距离活动结束只剩{}小时了\n最后一波抓紧哦".format(time_gap)
    elif time_gap < 5 and progress < 35:
        text_gap = "距离活动结束只剩{}天了\n你很弱欸".format(time_gap)
    elif progress > 133:
        text_gap = "距离活动结束还剩{}天呢\n你太秃了".format(time_gap)
    else:
        text_gap = "距离活动结束还剩{}天哦\n頑張れ(ง •_•)ง".format(time_gap)

    return text_gap


def read_configuration():
    """
    # 读取配置项
    """
    config = configparser.ConfigParser()
    config.read(r"config.ini", encoding="UTF-8")
    ongoing = int(config.get("ongoing_activities", "form"))
    if ongoing:
        name = config['ongoing_activities']['name']
        shop = config['shop']['all']
        mapid = dict(config.items('mapid'))
        mapid = eval(str(mapid).upper())
        stoptime = config['time']['stoptime']
        return True, (name, shop, mapid, stoptime)
    return (False,)


def change_configuration():
    """
    # 改写配置项
    """
    config = configparser.ConfigParser()
    config.read(r"config.ini", encoding="UTF-8")
    config.set('ongoing_activities', 'form', "0")
    config.write(open(r"config.ini", "w", encoding="UTF-8"))


def activites(completed, user_defined):
    """
    # 活动进度计算
    """
    info = read_configuration()
    if not info[0]:
        return (False,)

    name, shop, mapid, stoptime = info[1]

    shop = user_defined if user_defined else int(shop)

#    获取时间
    gap = time.mktime(time.strptime(stoptime, "%Y-%m-%d"))
    gap -= time.time() - 86400

    if completed >= 0 and completed <= shop:  # 如果在范围内
        bartext, booeolean = ["", "▏", "▍", "▋", "▊", "▉"], True
        for i in mapid:
            mapid[i] = (shop - completed)/int(mapid[i])
        progressn = completed/shop
        progress = progressn*100
        bar_num = int(progress // 10)
        barlist = bartext[5] * bar_num + bartext[int(progress % 10 / 2)]
        stuff_num = 10 - len(barlist)
        if stuff_num:  # 进度条填充
            barlist += "  " * (stuff_num - 1) + "▕"
        text_gap = typesetting(gap, progress)
    elif completed >= shop:  # 如果溢出
        progressn = completed/shop
        progress = progressn*100
        for i in mapid:
            mapid[i] = 0
        if completed - shop > 10000:
            text_gap = typesetting(gap, progress)
        else:
            text_gap = typesetting(gap, progress)
        progressn, barlist, booeolean = 1, "▉" * 10, True
    else:
        mapid = progressn = barlist = text_gap = None
        booeolean = False
    return True, (name, mapid, progressn, barlist, booeolean, text_gap)


async def progress_calculat(content, user_defined):
    """
    # 计算活动进度并排版
    """
    if not content.isdigit():
        return "已获得积分参数错误,应为整数"
    point = int(content)
    echo = "计算完成\n"
    info = activites(point, user_defined)
    if info[0]:
        name, schedule, progress, barlist, booeolean, gaptime = info[1]
        if booeolean:
            echo += "活动名：{}\n".format(name)
            for i in schedule:
                num = math.ceil(schedule[i])
                echo += "若只出击{}还需{}次\n".format(i, num)
            echo += "当前已获得{}积分\n已完成进度\n{} {:.2%}\n{}".format(point, barlist, progress, gaptime)
        else:
            echo = "你TMD不要瞎JB填, Please"
    else:
        echo = "暂时没有开启的活动哦"
return echo