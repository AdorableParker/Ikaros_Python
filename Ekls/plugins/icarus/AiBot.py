import random
from .My_comparator import Chinese_compare, Keyword_extraction
from plugins.tool.date_box import sql_read, sql_write, sql_rewrite

def selection(dedicated_corpus, max_ratio, response, user_input):
    for other_statement in dedicated_corpus:
        ratio = Chinese_compare(user_input, other_statement[1])
        if ratio > max_ratio:
            max_ratio = ratio 
            response = [other_statement[0]]
    
        elif ratio == max_ratio:
            response.append(other_statement[0])

    return max_ratio, response

def points(Qid, flag=False):
    score = sql_read("plugins/icarus/data.db", "favor_score", 'ID', Qid, 'score',)
    if not score:
        sql_write("plugins/icarus/data.db", "favor_score", (Qid, 50))
        data = (Qid, "", "", "", "", "", "", 0, 0)
        sql_write("plugins/icarus/data.db", "dedicated_corpus", data)
        score = [(50,)]
    score = score[0][0]
    if flag:
        new_score = score + random.randint(5,7)
    else:
        new_score = score + random.randint(-2,3)
    sql_rewrite("plugins/icarus/data.db", 'favor_score',"ID",Qid,"score", new_score)
    if new_score >= 700:    # 爱
        if score < 700:     # 晋升
            return "伊卡洛斯想和你永远在一起\n使用命令 ”只对我说“ + 空格 + 对话问题#回答内容，可以设置一项专属回答\n示范：只对我说 还记得我们的约定吗#我会永远记得的"
    elif new_score >= 300:  # 喜欢
        if score < 300:     # 晋升
            return "伊卡洛斯喜欢和你聊天\n使用命令 ”只对我说“ + 空格 + 对话问题#回答内容，可以设置一项专属回答\n示范：只对我说 还记得我们的约定吗#我会永远记得的"
        elif score >= 700:  # 降级
            return "伊卡洛斯觉得还不够了解你" 
    elif new_score >= 100:  # 熟悉
        if score < 100:     # 晋升
            return "伊卡洛斯愿意了解你了\n使用命令 ”只对我说“ + 空格 + 对话问题#回答内容，可以设置一项专属回答\n示范：只对我说 还记得我们的约定吗#我会永远记得的"
        elif score >= 300:  # 降级
            return "伊卡洛斯不再喜欢你了"
    elif new_score >=0:     # 陌生
        if score < 0:       # 晋升
            return "伊卡洛斯不再讨厌你了" 
        elif score >= 100:  # 降级
            return "伊卡洛斯开始疏远你了"
    else:                   # 讨厌
        if score >= 0:      # 降级
            return "伊卡洛斯开始讨厌你了"
    return ""

async def ai(user_input, Qid):
    keys = Keyword_extraction(user_input)

    text = points(Qid)

    max_ratio = 0
    response = []

    dedicated_corpus = sql_read("plugins/icarus/data.db", "dedicated_corpus", 'ID', Qid)[0]
    
    if dedicated_corpus and dedicated_corpus[7]:
        corpus = []
        for i in range(1, dedicated_corpus[7]+1):
            corpus.append((dedicated_corpus[i+3],dedicated_corpus[i]))
        max_ratio, response = selection(corpus, max_ratio, response, user_input)

        if max_ratio >= 0.7:
            return random.choice(response), text

    for i in keys:
        dedicated_corpus = sql_read("plugins/icarus/data.db", "universal_corpus", 'keys', i)
        max_ratio, response = selection(dedicated_corpus, max_ratio, response, user_input)

        if max_ratio >= 0.5:
            return random.choice(response), text

    for i in keys:
        dedicated_corpus = sql_read("plugins/icarus/data.db", "universal_corpus", 'question', '%{}%'.format(i[1]), link="LIKE")
        max_ratio, response = selection(dedicated_corpus, max_ratio, response, user_input)

        if max_ratio >= 0.5:
            return random.choice(response), text
    
    response = "你在说什么，我怎么听不懂\n(○´･д･)ﾉ"
    return response, text
    
async def training(Question, Answer, Qid, only_to_me=False):

    if only_to_me:
        score = sql_read("plugins/icarus/data.db", "favor_score", 'ID', Qid, 'score',)[0][0]
        if score >= 700:
            max_index = 3
        elif score >= 300:
            max_index = 2
        elif score >= 100:
            max_index = 1
        else:
            return "哈？！只对你说，你想得美\n(＃‘д´)ﾉ\n[好感度不足]"

        current_index, end_index = sql_read("plugins/icarus/data.db", "dedicated_corpus", 'ID', Qid, 'current, end')[0]
        if max_index > current_index:                                                            # 可用槽数大于已用槽数
            r_index = current_index 
            current_index += 1                                                                   # 已用槽数 +1    
            sql_rewrite("plugins/icarus/data.db", 'dedicated_corpus',"ID",Qid,"current", current_index)  # 更新已用槽记录
            response = "嗯嗯，我只和你说哦的\nヾ(^▽^*)))"
        elif max_index <= current_index:                                                         # 可用槽数小于或等于已用槽数
            r_index = end_index                                                                 
            end_index = 0 if end_index + 2 > max_index else end_index + 1                        # 最旧槽更新为可用槽中最旧的
            sql_rewrite("plugins/icarus/data.db", 'dedicated_corpus',"ID",Qid,"current", max_index)  # 更新已用槽为可用槽
            sql_rewrite("plugins/icarus/data.db", 'dedicated_corpus',"ID",Qid,"end", end_index)          # 更新最旧槽记录
            response = "我只能记住最后{}条只给你的回答，之前的都忘光光惹\n ≧ ﹏ ≦".format(max_index)
        sql_rewrite("plugins/icarus/data.db", 'dedicated_corpus',"ID",Qid,"question{}".format(r_index), Question)
        sql_rewrite("plugins/icarus/data.db", 'dedicated_corpus',"ID",Qid,"answer{}".format(r_index), Answer)
        
    else:
        data = (Answer, Question, Keyword_extraction(Question,1)[0])
        sql_write("plugins/icarus/data.db", "universal_corpus", data)
        points(Qid,flag=True)
        response = random.choice(("伊卡洛斯记住了你的话，因为你的认真教导，好感度上升了", 
                                  "伊卡洛斯记住了你的话，你教学的时候太严厉了，好感度下降了", 
                                  "这样的吗，我大概记住了\nฅ( ̳• ◡ • ̳)ฅ",
                                  "伊卡洛斯喜欢学习\nヾ(◍°∇°◍)ﾉﾞ",
                                  "虽然不太懂，但是伊卡洛斯还是把你教的知识记在了心里"))
    return response