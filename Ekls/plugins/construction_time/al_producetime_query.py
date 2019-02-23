from plugins.tool.data_box import sql_read


async def al_query_time(key_name):
    """
    # 以名字为索引,查询建造时间
    # 参数：
    # key_name*    索引名
    # 返回格式(str)：
    # "name":"time"
    """
    result = sql_read("User.db", "AzurLane_construct_time",
                      "Currentname", key_name)
    if not result:
        result = sql_read("User.db", "AzurLane_construct_time",
                          "Usedname", key_name)
    try:
        result = list(result[0])
    except IndexError:
        output = "该船名未收录或无法建造"
    else:
        output = "和谐名：{0[1]}\n原名：{0[0]}\n建造时长：{0[2]}".format(result)
    return output


async def al_query_name(key_time):
    """
    # 以时间为索引,查询可能船只名
    # 参数：
    # key_time*    索引名
    # 返回格式(str)：
    # '以下舰船符合建造时长 key_time :\n name1 \n name2 \n name3...'
    """
    result = sql_read("User.db", "AzurLane_construct_time", "time", key_time)
    name_list = "符合建造时长 %s 的舰船有：" % key_time
    for name in result:
        name_list += "\n" + name[0] + "        替代名：" + name[1]
    return name_list
