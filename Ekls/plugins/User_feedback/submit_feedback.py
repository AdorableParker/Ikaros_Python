import os
import time

async def submit_feedback(content_feedback, id, group_id):
    with open('Feednack.log', 'a') as file:
        file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        file.write("\ninfo:{}\nQQ:{}\nGroup_id:{}".format(content_feedback, id, group_id))
        file.close()