# -*- coding: utf-8 -*-
"""
# 小加加周期检测
"""
import time

from plugins.tool import data_box

from plugins.tool import crawler


def update_check(uid):
    """
    # 检测B博是否更新
    """
    update_data = crawler.get_trend(uid, False)  # 获取动态信息
    print(update_data)
    update_time = data_box.sql_read("User.db", "Crawler_update_time", "update_url", uid, field="update_time")[0]  # 获取历史时间戳

    if update_data[2] > update_time[0]:  # 对比时间戳
        text_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(update_data[2]))  # 时间戳格式化
        data_box.sql_rewrite("User.db", "Crawler_update_time", "update_url", uid,
                             "update_time", str(update_data[2]))  # 更新历史时间戳

        echo = "最新动态:\n{0[0]}\n{0[1]}\n{1} 于 {2} 发布至 BiliBili 动态".format(update_data, update_data[-1], text_time)  # 发表最新动态
        return True, echo
    return False, ""


if __name__ == "__main__":
    print(update_check("233114659"))