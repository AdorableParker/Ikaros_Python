import requests
import json

async def get_run_coderesult(langunges, code):
    headers = {
    'Authorization': 'Token 90d6042c-75c4-44fc-8f39-3fa1ccc5868d',
    'Content-type': 'application/json',
    }
    data = {
        "files": [{
            "name": "Main.{}".format(langunges[1]),
            "content": "{}".format(code)
            }]
        }
    data = json.dumps(data) 
    response = requests.post('https://run.glot.io/languages/{}/latest'.format(langunges[0]), headers=headers, data=data)
    response = json.loads(response.text)
    stdout, stderr = response["stdout"], response["stderr"]
    if stderr:
        return stderr
    if stdout:
        output = stdout
    else:
        output = "运行正常，代码无输出"
    return output