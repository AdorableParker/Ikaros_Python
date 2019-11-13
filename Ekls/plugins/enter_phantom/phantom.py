from PIL import Image
import numpy as np

def phantom():
    imgA, imgB = Image.open("A.jpg"), Image.open("B.jpg")
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
    
    def CheckRange(array):
    
        array = np.around(array)
        array[array > 255] = 255
        array[array < 0] = 0
    
        return array
    
    aRGB, bRGB = CheckRange(aRGB), CheckRange(bRGB)
    
    alpha = CheckRange(255 - aRGB + bRGB)
    alpha[alpha == 0] = 255
    imgArray = CheckRange(bRGB / alpha * 255)
    
    RGBA = np.uint8(np.hstack((imgArray, imgArray, imgArray, alpha)))
    outimgarray = RGBA.reshape(min_W, min_H, 4)
    outimg = Image.fromarray(outimgarray)
    return outimg


if __name__ == "__main__":
    outimg = phantom()
    outimg.save("out.png")