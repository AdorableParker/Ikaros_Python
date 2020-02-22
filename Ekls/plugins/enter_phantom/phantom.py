import requests
import ujson
from PIL import Image
import numpy as np
from io import BytesIO

async def phantom(img_A, img_B):

    imgA = Image.open(BytesIO(img_A))
    imgB = Image.open(BytesIO(img_B))

    imgA_array, imgB_array = np.array(imgA), np.array(imgB)
    A_Bsize = np.array([imgA_array.shape, imgB_array.shape])
    
    min_W, min_H, _ = A_Bsize.min(0)
    newimgA_array = np.array(imgA_array[:min_W, :min_H])
    newimgB_array = np.array(imgB_array[:min_W, :min_H])
    newimgA_array = newimgA_array.reshape(min_W * min_H, 3)
    newimgB_array = newimgB_array.reshape(min_W * min_H, 3)
    
    aR, aG, aB = np.hsplit(np.uint16(newimgA_array), 3)
    bR, bG, bB = np.hsplit(np.uint16(newimgB_array), 3)
    aRGB = np.right_shift(aR*76+aG*151+aB*28,8)
    bRGB = np.right_shift(bR*76+bG*151+bB*28,8)
    
    MeanaA = np.mean(aRGB,axis=0)
    MeanaB = np.mean(bRGB,axis=0)
    if MeanaA < MeanaB:
        aRGB,bRGB = bRGB,aRGB
        Outmin, Outmax = MeanaA, MeanaB
    else:
        Outmin, Outmax = MeanaB, MeanaA
    
    aRGB = (255 - Outmin) / 255 * aRGB + Outmin
    bRGB = Outmax / 255 * bRGB
    
    aRGB, bRGB = CheckRange(aRGB), CheckRange(bRGB)
    
    alpha = CheckRange(255 - aRGB + bRGB)
    alpha[alpha == 0] = 255
    imgArray = CheckRange(bRGB / alpha * 255)
    
    RGBA = np.uint8(np.hstack((imgArray, imgArray, imgArray, alpha)))
    outimgarray = RGBA.reshape(min_W, min_H, 4)
    outimg = Image.fromarray(outimgarray)
    imgByteArr = BytesIO()
    outimg.save(imgByteArr, 'jpeg')
    return imgByteArr.getvalue()


async def up_img(file):
    headers = {}
    files = {
    	'smfile':file
    }
    result = requests.post("https://sm.ms/api/v2/upload",files=files,headers=headers)
    result = ujson.loads(result.text)
    if result['success']:
        return result['data']['url']
    else:
        if "Image upload repeated limit" in result['message']:
            return result['message'].split(":", 1)[1].strip()
        return "图片上传失败\n" + result['message']


async def getimg(url):
    try:
        response = requests.get(url)
    except:
        return False
    if response.status_code == 404:
        return False
    return response.content

def CheckRange(array):
    
    array = np.around(array)
    array[array > 255] = 255
    array[array < 0] = 0
    
    return array


if __name__ == "__main__":
    outimg = phantom()
    outimg.save("out.png")