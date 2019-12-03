from requests_futures.sessions import FuturesSession
import ujson


error_info = {
    "INVALID_SEARCH":"无效搜索",
    "INVALID_FIELDS":"无效字段",
    "SEARCH_NOT_SPECIFIED":"参数为空",
    "SEARCH_NOT_SPECIFIED":"没有参数用户ID的搜索参数",
    "INVALID_APPLICATION_ID":"无效的应用密钥,请联系管理员",
    "REQUEST_LIMIT_EXCEEDED":"超出了请求限制",
    "SOURCE_NOT_AVAILABLE":"数据源不可用",
    "APPLICATION_IS_BLOCKED":"申请被主管部门阻止",
    "METHOD_NOT_FOUND":"方法无效",
    "METHOD_DISABLED":"方法被禁用",
    "NOT_ENOUGH_SEARCH_LENGTH":"参数长度不足",
    "INVALID_LANGUAGE": "返回语言无效"
}

extra = {
    "军团":"statistics.club",
    "单人剧情":"statistics.oper_solo",
    "组队剧情":"statistics.oper_div",
    "组队困难剧情":"statistics.oper_div_hard",
    "人机":"statistics.pve",
    "单排":"statistics.rank_solo",
    "双排":"statistics.rank_div2",
    "三排":"statistics.rank_div3",
}

translate = {

    "wins": "胜场",
    "losses": "败场",
    "draws": "平局",
    "battles": "战斗次数",
    
    "frags": "击沉战舰",
    "survived_battles": "存活次数",
    "survived_wins": "胜利并存活次数",
    
    "damage_dealt": "总计造成伤害",
    "art_agro": "总计造成潜在伤害",
    "torpedo_agro": "鱼雷造成潜在伤害总计",
    "damage_scouting": "侦察下造成伤害总计",
    "planes_killed": "总计击落飞机",

    "max_frags_battle": "单局最多击杀",
    "max_damage_dealt": "最大单局造成伤害",

    "max_damage_scouting": "最大侦察伤害",
    "max_total_agro": "单局最大潜在伤害",
    "max_planes_killed": "单局最多击落飞机数",

}

ship_id = {
    "max_frags_ship_id": "单局最多击杀数的船",
    "max_planes_killed_ship_id": "单局使用舰载机最多击杀数的船",
    "max_damage_dealt_ship_id": "单局造成伤害最多的船",
    "max_scouting_damage_ship_id": "单局造成侦察伤害最多的船",
    "max_total_agro_ship_id": "单局受到潜在伤害最多的船",
    "max_suppressions_ship_id": "损坏敌方设备最多的船",
    "max_ships_spotted_ship_id": "获得最多点亮缎带的船",
    "max_xp_ship_id": "获得经验最多的船",
    }

device_detail = {
    "main_battery":"主炮",
    "second_battery": "副炮",
    "torpedoes": "鱼雷",
    "aircraft": "舰载机",
    "ramming": "撞击"
}

device_detail_count = {				
    "max_frags_battle": "单局最多击杀",
    "frags": "击杀总数",
    "hits": "命中数",
    "max_frags_ship_id": "最多击杀数的船",
    "shots": "射击总数"
}



params = {
    'application_id': '2363bdcf3dbbff93212c59286f0849e1',
    }


async def getid(name):

    params['search'] = name
    params['type'] = 'exact'
    session = FuturesSession()
    response = session.get('https://api.worldofwarships.asia/wows/account/list/', params=params).result()
    del params['search']
    del params['type']
    
    useridlist = ujson.loads(response.text)

    if useridlist['status'] == "error":
        return error_info[useridlist['error']['message']], False
    print(useridlist)
    if not useridlist['data']:
        return "没有找到名为{}的账号".format(name), False
    return useridlist['data'][0], True

async def infoInquire(name, mode):

    info, err = await getid(name)
    if not err:
        return info, False

    params['account_id'] = info["account_id"]
    params['extra'] = extra.get(mode,"")
    params['fields'] = extra.get(mode,"statistics.pvp")

    session = FuturesSession()
    response = session.get('https://api.worldofwarships.asia/wows/account/info/', params=params).result()
    
    del params['extra']
    del params['fields']
    
    data = ujson.loads(response.text)['data'][str(info["account_id"])]
    
    return await infoTranslate(data, extra.get(mode,"statistics.pvp"))
    
    
async def infoTranslate(info, mode):
    mode = mode.split(".")[-1]
    info = info['statistics'][mode]
    
    if not 'damage_dealt' in info:
        return "无相关记录信息", False

    outinfo = {}
    for key in translate:
        if key in info:
            outinfo[translate[key]] = info[key]
    for key in device_detail:
        device = info.get(key, "")
        for keys in device_detail_count:
            if keys in device:
                if keys == "max_frags_ship_id":
                    device[keys] = await shipName(device[keys])
                outinfo["{} {}".format(device_detail[key], device_detail_count[keys])] = device[keys]
                

    for key in ship_id:
        if key in info:
            outinfo[ship_id[key]] = await shipName(info[key])

    outinfo["胜率"] = "{:.2%}".format(outinfo['胜场']/outinfo['战斗次数'])
    if mode.split("_")[0] == "oper":
        for key in info["wins_by_tasks"]:
            outinfo["{}星取胜场数".format(key)] = info["wins_by_tasks"][key]
    else:
        outinfo["场均伤害"] = "{:.2f}".format(outinfo['总计造成伤害']/outinfo['战斗次数'])
        outinfo["主炮命中率"] = "{:.2%}".format(outinfo['主炮 命中数']/outinfo['主炮 射击总数'])
        outinfo["鱼雷命中率"] = "{:.2%}".format(outinfo['鱼雷 命中数']/outinfo['鱼雷 射击总数'])

    return outinfo, True
    
    
async def shipName(ship_id):
    
    if not ship_id:
        return "无"
    params["fields"] = "name"
    params['language'] = 'zh-cn'
    params['ship_id'] = ship_id


    session = FuturesSession()
    response = session.get('https://api.worldofwarships.ru/wows/encyclopedia/ships/', params=params).result()

    del params['fields']   
    del params['language']
    del params['ship_id']

    return ujson.loads(response.text)['data'][str(ship_id)]['name']