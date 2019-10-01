import requests
import ujson

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
    data = ujson.dumps(data) 
    response = requests.post('https://run.glot.io/languages/{}/latest'.format(langunges[0]), headers=headers, data=data)
    response = ujson.loads(response.text)
    output = "output:\n"
    for i in response:
        output += response[i] + "\n"
    return output


'''
    try:
        if "stdout" in response:
            stdout, stderr = response["stdout"], response["stderr"]
        else:
            output = response['message']
            return output
    except:
        print("-------------------------\n\n",response,"\n\n-------------------------")
        raise
    if stderr:
        return stderr
    if stdout:
        output = stdout
    else:
        output = "运行正常，代码无输出"
    return output
'''