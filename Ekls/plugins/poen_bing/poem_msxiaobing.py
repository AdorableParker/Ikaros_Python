import requests
import base64
import json
from requests_toolbelt import MultipartEncoder

def get_img(img_url):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    response = requests.get(img_url, headers=headers)
    img = base64.b64encode(response.content)
    return img

async def writing(img_url, text=""):
	headers = {
		'Origin': 'https://poem.msxiaobing.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
		'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary8m1IZnXyymX0aBvc',
		'Accept': '*/*',
		'Referer': 'https://poem.msxiaobing.com/',
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',
	}

	files = {'image': get_img(img_url),
			 'userid': 'GDUmNCE1QzLZTCg1eTFVM8o0FU7nMF1K2TBFMCFL0bRLAA',
			 'text': text,
			 'guid': '1e46152a-537e-4e76-96e0-6f59f0c5e459'}

	m = MultipartEncoder(files, boundary='----WebKitFormBoundary8m1IZnXyymX0aBvc')

	response = requests.post('https://poem.msxiaobing.com/api/upload', headers=headers, data=m.to_string())
	result = response.json()
	production = []
	for i in result["OpenPoems"]:
		production.append(i["PoemContent"])
	return production

if __name__ == "__main__":
	img_url = "https://gchat.qpic.cn/gchatpic_new/764780622/787211538-2670411425-8E63EB1008CFCAF36236C3D14AD36981/0?vuin=2951899724&amp;amp;term=2"
	writing(img_url)