from distutils import dir_util
from keras.models import load_model
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import scipy.io
from scipy.signal import argrelextrema
from scipy.ndimage.filters import gaussian_filter
import tensorflow as tf

import time

# 最初步的ROI (把原圖黑邊切掉) 
x = [200, 600]
y = [40, 650]

# 取得資料夾中圖片並丟進predict
def load_images_from_folder(path):
  files= os.listdir(path) #得到資料夾下的所有檔名稱
  #orginal size(576, 768, 3)
  for root, dirs, files in os.walk(path):
        for file in files:
            # 這邊是每個資料夾挑編號10 20 30的圖片來做測試，可以自己改數字
            for i in range(3):
                if str(i*10+10)+".png" == file:
                    fullpath = os.path.join(root, file)
                    img = np.array(cv2.imread(fullpath, cv2.IMREAD_GRAYSCALE)) # 改為灰階
                    start_time = time.time() # 用來計算時間
                    result = predict(img) # 丟原圖進去產生result
                    print("Whole: %s seconds " % round((time.time() - start_time),3))
                    print("==========================")

                    show_results(img, result)
  plt.show()

# 計算top、bot裁切軸
def get_cropImg_axis(img):

    # 把img每個row所有pixel的intensity value相加存進row_sum
    row_size = img.shape[0]
    row_sum = np.zeros(row_size)
    for i in range(row_size):
        row_sum[i] = np.sum(img[i,:])

    # 用gausssian filter使結果平滑(c++裡面用的是triangular smooth)    
    row_sum = gaussian_filter(row_sum, sigma=7)

    # 從row_sum中找出所有的local maximum
    local_max = argrelextrema(row_sum, np.greater)
    max_value =  row_sum[local_max]   
    max_value = np.sort(max_value)

    # 如果local maximum的數量>=3，就取出值前三大的local maximum，假設為血管壁位置
    # (這邊看不懂可以看專題展影片)
    if len(max_value)>=3:
        max1 = max_value[-1]
        max2 = max_value[-2]
        max3 = max_value[-3]
        for i in range(row_size):
            if row_sum[i] == max1:
                wall1 = i
            elif row_sum[i] == max2:
                wall2 = i
            elif row_sum[i] == max3:
                wall3 = i
        # 上下血管壁位置取中間即為血管軸
        # 算出三組可能為血管軸的位置，找出intensity value最小者
        # 並記錄下此狀況下，血管壁的位置
        axis1 = (wall1 + wall2)//2
        axis2 = (wall2 + wall3)//2
        axis3 = (wall1 + wall3)//2
        axis = axis1
        wallUp = wall1
        wallDown = wall2
        if row_sum[axis]>row_sum[axis2]:
            axis = axis2
            wallUp = wall2
            wallDown = wall3
        if row_sum[axis]>row_sum[axis3]:
            axis = axis3
            wallUp = wall1
            wallDown = wall3

    #如果local maximum的數量>=，兩血管壁位置取中間即為血管軸
    elif len(max_value)>=2:
        max1 = max_value[-1]
        max2 = max_value[-2]
        for i in range(row_size):
            if row_sum[i] == max1:
                wall1 = i
            elif row_sum[i] == max2:
                wall2 = i
        axis = (wall1 + wall2)//2
        wallUp = wall1
        wallDown = wall2

    else:
        print('crop error')
        return

    if wallUp>wallDown:
        temp = wallDown
        wallDown = wallUp
        wallUp = temp
    axis = int(axis)#
    # 透過血管壁與軸的位置做裁切，裁切邊界必須在img內
    cropLineUp = wallUp-(axis-wallUp)   
    if cropLineUp<0:
        cropLineUp = 0
    cropLineDown = wallDown+(wallDown-axis) 
    if cropLineDown>img.shape[0]:
        cropLineDown = img.shape[0]

    # 回傳裁切後圖片以及裁切軸
    cropImgDown = img[axis:cropLineDown,:]
    cropImgUp = img[cropLineUp:axis,:]
    cropImgUp = cv2.flip(cropImgUp, 0)

    return cropImgUp, cropImgDown, cropLineUp, axis, cropLineDown

#img轉成sobel
def imgsToSobel(img):
  sobely = cv2.Sobel(img,cv2.CV_8U,0,1,ksize=3)
  return np.array(sobely)
def imgsToPrewitt(img):
  #kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
  kernelx = np.array([[-1.,-1.,-1.],[0.,0.,0.],[1.,1.,1.]], dtype=np.float64)
  kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float64)
  x = cv2.filter2D(img.astype(np.float64), -1, kernelx,borderType = cv2.BORDER_CONSTANT)
  y = cv2.filter2D(img.astype(np.float64), -1, kernely,borderType= cv2.BORDER_CONSTANT)
  x = np.clip(x, 0, 255).astype(np.uint8)
  y = np.clip(y, 0, 255).astype(np.uint8)

  Prewitt = y-x
  return 255-Prewitt
# 將原圖和sobel合併成list並return
def produce_preprocessed_img(img):
  sobel = imgsToSobel(img)
  prewitt = imgsToPrewitt(img)
  img2 = np.array([prewitt, sobel])
  return img2

# 將prewitt和sobel丟進tflite model 分割
def LiteSeg(prewitt_img, sobel_img):
    # 整理好格式 & 尺寸
    input1 = sobel_img.reshape(-1,128,512,1).astype("float32")/255
    input2 = prewitt_img.reshape(-1,128,512,1).astype("float32")/255
    
    print(np.array([input1, input2]).shape)

    # 設定模型輸入格式 並輸入至模型
    interpreter.set_tensor(input_details[0]['index'], input1)
    interpreter.set_tensor(input_details[1]['index'], input2)
    interpreter.invoke()

    # 取得分割結果並整理格式 & 尺寸
    seg = interpreter.get_tensor(output_details[0]['index'])
    seg = seg.reshape(128,512)
    seg= (seg*255).astype(np.uint8)

    # 分割結果intensity value < 40的設成0 其餘設255
    ret, seg = cv2.threshold(seg, 40, 255, cv2.THRESH_BINARY)
    return seg

# 去除假影 (參數: 圖片、過黑區域的強度值、去除多少百分位以下(假影臨界)的pixel)
def eli_noise(img, dark, percentile):
    # 先把過黑區域濾除(只留下>dark的部分)
    remove_dark = img[img>dark]
    # 在剩餘pixel中 計算假影臨界
    minus = np.percentile(remove_dark, percentile)
    # 把假影臨界以下的pixel設成0 其餘縮放回0-255的區間(專題展影片內有示意圖)
    multiply = 255/(255-minus)
    img = np.where(img >= minus, (img-minus)*multiply, 0)
    return img  

# 分割出內膜
def predict(img):
  Resize = (512,128)
  original_size = img.shape
  
  # 裁切初步roi
  img = img[x[0]:x[1], y[0]:y[1]]

  # 找出裁切軸、上下半部圖片
  top, bot, LineUp, axis, LineDown = get_cropImg_axis(img)

  # 將top、bot(上下半部圖片)做前處理
  top = eli_noise(top, 20, 60)
  bot = eli_noise(bot, 20, 15)
  top_size = top.shape
  bot_size = bot.shape
  top = np.array(cv2.resize(top, Resize, interpolation = cv2.INTER_AREA))
  bot = np.array(cv2.resize(bot, Resize, interpolation = cv2.INTER_AREA))
  top2 = produce_preprocessed_img(top)
  bot2 = produce_preprocessed_img(bot)

  # 影像分割(top_mask和bot_mask分別是上下半部圖片分割後的結果)
  prewitt = top2[0]
  sobel_img = top2[1]
  top_mask = LiteSeg(prewitt, sobel_img)
  top_mask = cv2.flip(top_mask, 0)
  prewitt = bot2[0]
  sobel_img = bot2[1]
  bot_mask = LiteSeg(prewitt, sobel_img)

  # 將結果resize成原本的尺寸
  top_mask = cv2.resize(top_mask, (top_size[1], top_size[0]), interpolation = cv2.INTER_NEAREST)
  bot_mask = cv2.resize(bot_mask, (bot_size[1], bot_size[0]), interpolation = cv2.INTER_NEAREST)
  combined = np.append(np.array(top_mask), np.array(bot_mask), axis = 0)

  # 將結果貼回最原始影像(含有黑邊的原圖)中的位置
  topzero = np.zeros((x[0] + LineUp, top_size[1]))
  combined = np.append(topzero, combined, axis = 0)
  botzero = np.zeros((original_size[0] - (x[0] + LineDown), top_size[1]))
  combined = np.append(combined, botzero, axis = 0)#currently column is fully padded
  leftzero = np.zeros((combined.shape[0],y[0]))
  combined = np.append(leftzero, combined, axis = 1)
  rightzero = np.zeros((combined.shape[0],original_size[1]-combined.shape[1]))
  combined = np.append(combined, rightzero, axis = 1)

  return combined

# 顯示結果
def show_results(img, result):
  alpha = 0.5
  plt.imshow(img[x[0]:x[1],y[0]:y[1]],cmap='gray')
  plt.pause(0.05)
  overlap = cv2.addWeighted(img, alpha, result.astype(np.uint8), 1-alpha,0)
  overlap = overlap[x[0]:x[1],y[0]:y[1]]
  plt.imshow(overlap,cmap='gray')
  plt.pause(0.05)
#   plt.show()
#   print("-------------")
  
#########################################################
  
# 載入模型 並開始執行  
model_path = "./model0326_crop_Lite.tflite"
interpreter = tf.lite.Interpreter(model_path=model_path)
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
interpreter.allocate_tensors()

dir = "./"
load_images_from_folder(dir)