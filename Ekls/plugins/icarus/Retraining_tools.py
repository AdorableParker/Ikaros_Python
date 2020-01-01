from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import ujson
import os

# 训练
def in_data(trainer):
    trainer.train(
        "./my_export.json",
    )

# 导出
def out_data(trainer):
    trainer.export_for_training('./my_export.json')
    

while True:
    num = int(input("导出数据【1】 | 训练数据【2】 | 数据去重【3】 | 退出工具【任意】："))
    if num:
        break

Ai_bot = ChatBot(
    '伊卡洛斯',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.db'
)


trainer = ChatterBotCorpusTrainer(Ai_bot)       
        
        
if num == 1:
    out_data(trainer)
    print('导出完成')
    
elif num == 2:
    in_data(trainer)
    print('训练完成')
    
elif num == 3:
    out_data(trainer)
    with open('./my_export.json', 'r',encoding="utf-8") as f:
        data = ujson.loads(f.read())
        
    namelist = list(set(map(tuple, data['conversations'])))
    data['conversations'] = namelist
    
    with open('./my_export.json', 'w',encoding="utf-8") as R:
        R.write(ujson.dumps(data,ensure_ascii=False))
    os.remove('./database.db')
    os.remove('./sentence_tokenizer.pickle')

    Ai_bot = ChatBot(
        '伊卡洛斯',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            'chatterbot.logic.BestMatch'
        ],
        database_uri='sqlite:///database.db'
    )
    trainer = ChatterBotCorpusTrainer(Ai_bot)    

    in_data(trainer)
    print('去重完成')
    
else:
    exit()