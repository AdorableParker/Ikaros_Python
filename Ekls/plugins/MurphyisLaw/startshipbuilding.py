import random
import ujson
import time

async def startshipbuilding(buildtype, num):
    with open('./plugins/MurphyisLaw/namelist.json', 'r',encoding="utf-8") as f:
        data = ujson.loads(f.read())
    namelist = data[buildtype]
    buildresultlist = {}
    for i in range(num):
        time.sleep(0.1)
        rareProbability = random.randint(1,1000)
        if rareProbability <= 70:
            buildingrare="超稀有"
        elif rareProbability <= 190:
            buildingrare="精锐"
        elif rareProbability <= 450:
            buildingrare="稀有"
        else:
            buildingrare="普通"
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