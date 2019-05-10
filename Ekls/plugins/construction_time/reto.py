"""
# 正则工具箱
"""
import re


def r2n(string, key):
    """
    # 参数(标*为必填参数)：
    # string   待匹配字符串*
    # key    需匹配关键字列表*
    # 返回:
    # 匹配成功返回 匹配成功的内容
    # 匹配失败返回 None
    """
    rekey = key[0]
    for i in key[1:]:
        rekey = rekey + "|" + i
    out = re.search(rekey, string, flags=0)
    if out is not None:
        return out.group()
    return False
