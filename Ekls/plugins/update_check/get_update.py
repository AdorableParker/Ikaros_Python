# -*- coding: utf-8 -*-
"""
# 小加加周期检测
"""
import time

from plugins.tool import date_box

from plugins.tool import crawler


def update_check(uid):
    """
    # 检测B博是否更新
    """
    update_data = crawler.get_trend(uid, False)  # 获取动态信息
    update_time = date_box.sql_read("User.db", "Crawler_update_time", "update_url", uid, field="update_time")[0]  # 获取历史时间戳
    if update_data["code"] == 0: # 正常状况
        posted_time = update_data["posted_time"]
        if posted_time > update_time[0]:  # 对比时间戳
            text_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                      time.localtime(posted_time))  # 时间戳格式化
            date_box.sql_rewrite("User.db", "Crawler_update_time", "update_url", uid,
                                 "update_time", str(posted_time))  # 更新历史时间戳

            img_url = update_data.get("img","")
            main_body = update_data.get("main_body","")
            sign = update_data.get("sign", "")

            echo = "最新动态:\n{}\n{}\n{} 于 {} 发布至 BiliBili 动态".format(main_body, img_url, sign, text_time)  # 发表最新动态
            return True, echo
        return False, None
    elif update_data["code"] == 1:  # 连续三次错误返回
        return False, "本周期尝试获取动态信息失败超过三次，等待下一更新周期"
    else:  # 其他状况
        return False, "错误码尚未定义"


if __name__ == "__main__":
    print(update_check("233114659"))