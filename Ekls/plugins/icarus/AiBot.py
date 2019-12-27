from chatterbot import ChatBot


Ai_bot = ChatBot(
    '伊卡洛斯',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///plugins/icarus/database.db'
)

async def ai(user_input):
    response = str(Ai_bot.get_response(user_input))

    return response