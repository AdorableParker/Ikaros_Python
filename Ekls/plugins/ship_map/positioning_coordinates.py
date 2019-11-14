from plugins.tool.date_box import sql_read

MapID = ('原名', '和谐名', 
         '1-1', '1-2', '1-3', '1-4', 
         '2-1', '2-2', '2-3', '2-4', 
         '3-1', '3-2', '3-3', '3-4', 
         '4-1', '4-2', '4-3', '4-4', 
         '5-1', '5-2', '5-3', '5-4', 
         '6-1', '6-2', '6-3', '6-4', 
         '7-1', '7-2', '7-3', '7-4', 
         '8-1', '8-2', '8-3', '8-4', 
         '9-1', '9-2', '9-3', '9-4', 
         '10-1', '10-2', '10-3', '10-4', 
         '11-1', '11-2', '11-3', '11-4', 
         '12-1', '12-2', '12-3', '12-4', 
         '13-1', '13-2', '13-3', '13-4')

def al_query_coordinate(key_name):
    '''
    # 根据船名找地图
    '''
    resultlist = sql_read("User.db", "ship_map",
                      "Currentname", "*{}*".format(key_name), link = "GLOB")
    if not resultlist:
        resultlist = sql_read("User.db", "ship_map",
                          "Usedname", "*{}*".format(key_name), link = "GLOB")
    if resultlist:
        output = ""
        for name in resultlist:
            output += "原名：{0[0]}\t和谐名：{0[1]}\t可在以下地点打捞\n".format(name)
            for i, j in enumerate(name[2:], 2):
                if j:
                    output += MapID[i] + "\n"
    else:
        output = "该船名未收录或无法打捞"
    return output


def al_query_name(key_time):
    '''
    # 根据地图名找船
    '''
    result = sql_read("User.db", "ship_map", key_time, 1, "Usedname")
    if result:
        name_list = "\n %s 可以的打捞的舰船有：" % key_time
        for name in result:
            name_list += "\n" + name[0]
    else:
        name_list = "没有找到地图 %s 的信息" % key_time
    return name_list