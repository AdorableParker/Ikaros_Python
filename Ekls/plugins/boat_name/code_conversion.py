from plugins.tool.data_box import sql_read


async def code_name(name):
    """
    # 重樱船名对应表
    # 以名字或代号为索引对应代号或名字
    # 参数：
    # name*    索引
    # 返回格式(str)：
    # "name":"name"
    """
    result = sql_read("User.db", "Roster", "name", name)
    if not result:
        result = sql_read("User.db", "Roster", "code", name)
    try:
        result = list(result[0])
    except IndexError:
        toname = (False,)
    else:
        toname = (True, "和谐名：{0[0]}\t原名：{0[1]}".format(result))
    return toname
