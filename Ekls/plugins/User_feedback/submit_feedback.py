import os
import time

async def submit_feedback(content_feedback, id):
    with open('Feednack.log', 'a') as file:
        file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        file.write("\n{}\n{}\n".format(content_feedback, id))
        file.close()