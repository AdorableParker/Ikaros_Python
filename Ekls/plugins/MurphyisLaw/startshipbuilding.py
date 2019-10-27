import random
import ujson
import time

async def startshipbuilding(buildtype, num):
    with open('./plugins/MurphyisLaw/namelist.json', 'r',encoding="utf-8") as f:
        print(f)
        data = ujson.loads(f.read())
    namelist = data[buildtype]
    buildresultlist = {}
    for i in range(int(num)):
        time.sleep(random.random())
        rareProbability = random.randint(1,100)
        if rareProbability <= 7:
            buildingrare="超稀有"
        elif rareProbability <= 19:
            buildingrare="精锐"
        elif rareProbability <= 45:
            buildingrare="稀有"
        else:
            buildingrare="普通"
        ship = random.choice(namelist[buildingrare])
        buildresultlist[ship] = buildresultlist.setdefault(ship, 0) + 1
    buildresult = "船名\t\t次数\n-------------"
    for i in buildresultlist:
        buildresult += "\n{}\t{}".format(i,buildresultlist[i])
    return buildresult