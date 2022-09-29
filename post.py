from cmath import cos
from re import I
import cv2
import numpy as np

import time
start = time.time() #計算時間

#讀圖片
a = cv2.imread("./co1" + ".png")   #model predict結果
o = cv2.imread("./ca1" + ".png")   #原圖

#紀錄圖片大小
img_width = a.shape[1]
img_height = a.shape[0]
o_img_width = o.shape[1]
o_img_height = o.shape[0]

#前處理切割中縣 這裡先假設是0.5 實際上憲的座標會由前處理function傳過來
middle_line  = 0.5*img_height

newa = cv2.cvtColor(a,cv2.COLOR_BGR2GRAY)  #讀近來的圖轉黑白(這裡也只是因應自己做測試)
start = time.time() #計算時間

#opencv顯示圖片的寫法 1.建立window 2.調整window 3.顯示圖片在window上
cv2.namedWindow('window',0)
cv2.resizeWindow('window', img_width,img_height)
cv2.imshow('window',newa) #這裡為顯示轉換成黑白圖的model predict之結果

#threshhold 裡面的參數THRESH_BINARY可以讓值變成0or255
ret,thresh = cv2.threshold(newa,5,255,cv2.THRESH_BINARY)

#cv2.findContours 可以找到邊界並儲存在"contours"裡面，contours[i]裡面一個元素存著一個區域的邊界資訊，
# 圖片有兩個白色區域的話，contours.size = 2
contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
roi = []
rect = []
imt = []
upper_index = []
bottom_index = []
bound = [0,img_height,0,0]
flex = 10
#cv2.contourArea可以算一個區域的面積
#cv2.boundingRect可以算為成一個區域的最小矩形
#由前處理拿到的middleline找出血管上壁和下壁的可能範圍，存在bound[]裡
for c in range(len(contours)):
    if cv2.contourArea(contours[c]) > 150:
        (x,y,w,h) = cv2.boundingRect(contours[c])
        if (y < middle_line) and (y > bound[0]):
            bound[0] = y
            bound[2] = y+h
        elif (y + h > middle_line) and (y+h < bound[1]):
            bound[1] = y
            bound[3] = y+h

#將血管壁附近的contours區域存到roi裡(面積太小的不存)
for c in range(len(contours)):
    if cv2.contourArea(contours[c]) > 10: 
        (x,y,w,h) = cv2.boundingRect(contours[c])
        if (y < middle_line) and ((y > bound[0] - flex)or(y+h > bound[0]-5)) and (y < bound[2]):
            a = cv2.drawContours(a, contours, c, (0, 0, 255), 2)
            roi.append(c)
            upper_index.append(c)
        elif (y + h > middle_line) and ((y+h < bound[3] + flex)or(y<bound[3]+5)) and (y+h > bound[1]):
            a = cv2.drawContours(a, contours, c, (0, 0, 255), 2)
            roi.append(c)
            bottom_index.append(c)

#將roi資訊存起來
for r in range(len(roi)):
    (x, y, w, h) = cv2.boundingRect(contours[r])
    rect.append((x,y,w,h))
    imt.append(y+h)
average_imt = 0
count = 0

#計算IMT厚度
for i in range(len(imt)):
    if imt[i] > middle_line:
        average_imt += cv2.contourArea(contours[roi[i]])
        count += rect[i][2]
average_imt /= count
print("average IMT = ","{:.4f}".format(average_imt),"(pixel)")
print("IMT = ","{:.4f}".format(average_imt/16.66),"(mm)")

#################count LD/IAD
c = np.zeros((a.shape[1],4))
Ratio = []
averageRatio = 0
medianRatio = 0
minRatio = 0
if len(upper_index) == 0:
    print("No upper boundary was labeled!")    #上部沒有標記到    
else:
    #在上血管壁的rect裡面看是否為黑白交接處，是的話記到c矩陣裡
    for u in range(len(upper_index)):
        (x,y,w,h) = cv2.boundingRect(contours[upper_index[u]])
        temp = y+h
        for j in range(x,x+w):
            for i in range(y,y+h):
                if thresh[i][j]<thresh[i+1][j]:
                    c[j][0] = i
                    break
            for i in range(0,h):
                if thresh[temp-i][j]<thresh[temp-i-1][j]:
                    c[j][1] = temp - i
                    break
    #在下血管壁的rect裡面看是否為黑白交接處，是的話記到c矩陣裡
    for b in range(len(bottom_index)):
        (x,y,w,h) = cv2.boundingRect(contours[bottom_index[b]])
        temp = y+h
        for j in range(x,x+w):
            for i in range(y,y+h):
                if thresh[i][j] < thresh[i+1][j]:
                    c[j][2] = i
                    break
            for i in range(0,h):
                if thresh[temp-i][j] < thresh[temp-i-1][j]:
                    c[j][3] = temp - i
                    break
    count = 0
    #計算average median min的ratio
    for i in range(a.shape[1]):
        if c[i][0]>0 and c[i][1]>0 and c[i][2]>0 and c[i][3]>0:
            Ratio.append((c[i][2] - c[i][1])/(c[i][3] - c[i][0]))
    averageRatio = sum(Ratio)/len(Ratio)
    print("averageRatio = ","{:.4f}".format(averageRatio))
    medianRatio = np.median(Ratio)
    print("medianRatio = ","{:.4f}".format(medianRatio))
    minRatio = np.min(Ratio)
    print("minRatio = ","{:.4f}".format(minRatio))

#因為標記在原圖上的只有框框，所以將原本白色的地方變成黑色的讓等等疊圖的時候只疊到框
for i in range(img_height):
    for j in range(img_width):
        if a[i][j][0] == 255:
            a[i][j] = (0,0,0)  

#只有ROI的框框
cv2.namedWindow('window2', 0)
cv2.resizeWindow('window2', img_width,img_height)
cv2.imshow('window2',a)

#前處理的切割的上緣(這份code現在只有用到第一個)
croplineup = [77, 96, 93, 92, 119, 120, 96, 89, 122, 92, 89, 91, 96]
# croplineup = [5, 55, 5, 76, 26, 95, 53, 55, 95, 109, 247, 200, 10]

#將框框以及原圖疊起來
imgCrop = o[croplineup[0]:croplineup[0]+img_height,0:img_width]
imgAdd = cv2.add(imgCrop,a)
alpha,beta,gamma = 1.0,1.0,0.0
imgAddW = cv2.addWeighted(imgCrop,alpha,a,beta,gamma)
imgAddM=np.array(o)
imgAddM[croplineup[0]:croplineup[0]+img_height,0:img_width] = imgAddW
cv2.namedWindow('window3', 0)
cv2.resizeWindow('window3', o_img_width,o_img_height)
cv2.imshow('window3',imgAddM)
print("time cost ",(time.time() - start),"sec")  #拿來算時間用的
cv2.waitKey(0)