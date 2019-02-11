# -*- coding: utf-8 -*-
"""
# 小加加周期检测
"""
import time

from .data_box import sql_read, sql_rewrite
from .crawler import get_trend


def update_check():
    """
    # 检测B博是否更新
    """
    update_data = get_trend('233114659', False)  # 获取动态信息
    update_time = sql_read("User.db", "Crawler_update_time", "update_url", "Bilibili", field="update_time")[0]  # 获取历史时间戳

    if update_data[2] > update_time[0]:  # 对比时间戳
        text_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(update_data[2]))  # 时间戳格式化
        sql_rewrite("User.db", "Crawler_update_time", "update_url", "Bilibili",
                             "update_time", str(update_data[2]))  # 更新历史时间戳
        echo = "小加加最新动态:\n" + update_data[0] + "\n" + update_data[1]
        echo += "\n于 " + text_time + " 发布至 BiliBili 动态"  # 发表最新动态
        return True, echo
    return False, ""
