import random
import ujson
import time

def judgment(buildtype, namelist):

    probability_list = {
        "轻型":(70,190,450), 
        "重型":(70,190,700), 
        "特型":(70,190,700),
        "限时":(70,190,700)
        }

    rareProbability = random.randint(1,1000)
    if buildtype == "限时":
        special_probability = 0
        for j in namelist:
            special_probability += int(j)
            if rareProbability <= special_probability:
                ship = random.choice(namelist[j])
                return ("特殊类型", ship)
    if rareProbability <= probability_list[buildtype][0]:
        buildingrare="超稀有"
    elif rareProbability <= probability_list[buildtype][1]:
        buildingrare="精锐"
    elif rareProbability <= probability_list[buildtype][2]:
        buildingrare="稀有"
    else:
        buildingrare="普通"
    return buildingrare

async def startshipbuilding(buildtype, num):
    with open('./plugins/MurphyisLaw/namelist.json', 'r',encoding="utf-8") as f:
        data = ujson.loads(f.read())
    namelist = data[buildtype]
    buildresultlist = {}
    for i in range(num):
        time.sleep(0.1)
        buildingrare = judgment(buildtype, namelist)
        if buildtype == "限时":
            if type(buildingrare) == tuple:
                buildingrare, ship = buildingrare
            else:
                ship = buildingrare

            if buildingrare in buildresultlist:
                if ship in buildresultlist[buildingrare]:
                    buildresultlist[buildingrare][ship] += 1
                else:
                    buildresultlist[buildingrare][ship] = 1
            else:
                buildresultlist[buildingrare] = {ship:1}

        else:
            ship = random.choice(namelist[buildingrare])
            if buildingrare in buildresultlist:
                if ship in buildresultlist[buildingrare]:
                    buildresultlist[buildingrare][ship] += 1
                else:
                    buildresultlist[buildingrare][ship] = 1
            else:
                buildresultlist[buildingrare] = {ship:1}

    buildresult = "船名　　　　　　　次数\n==============="
    for i in buildresultlist:
        buildresult += "\n{:　<7}共计:{}艘\n— — — — — — —".format(i, sum(buildresultlist[i].values()))
        for j in buildresultlist[i]:
            buildresult += "\n{:　<10}{}".format(j,buildresultlist[i][j])
        buildresult += "\n==============="
    return buildresult

