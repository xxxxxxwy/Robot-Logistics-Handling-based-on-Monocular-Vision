#这个包做的是颜色识别相关的各种函数
# 导入所需模块
import cv2 as cv
import numpy as np
import imutils

#hsv
#red (0,43,46,10,255,255)or(156,43,46,180,255,255)
#yellow(26,43,46,34,255,255)
#green(35,43,46,77,255,255)
#white(0,0,221,180,30,255)



def hsvtest(h1,s1,v1,h2,s2,v2):#输入hsv上限限，返回相对位置（1，-1，0）或者未找到（3）
    # 打开摄像头
    cap = cv.VideoCapture(0)#解决了一个警告
    #cap = cv.VideoCapture(0,cv.CAP_DSHOW)#解决了一个警告

    while True:
 
        # 读取每一帧
        _, frame = cap.read()
        # 重设图片尺寸以提高计算速度
        frame = imutils.resize(frame, width=600)
        # 进行高斯模糊
        blurred = cv.GaussianBlur(frame, (11, 11), 0)
        # 转换颜色空间到HSV
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
        # 定义无图的HSV阈值
        lower_red = np.array([h1, s1, v1])
        upper_red = np.array([h2, s2, v2])
        # 对图片进行二值化处理
        mask = cv.inRange(hsv, lower_red, upper_red)
        # 腐蚀操作
        mask = cv.erode(mask, None, iterations=2)
        # 膨胀操作，先腐蚀后膨胀以滤除噪声
        mask = cv.dilate(mask, None, iterations=2)
 
        cv.imshow('mask', mask)
 
        # 寻找图中轮廓
        cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
 
        # 如果存在至少一个轮廓则进行如下操作
        if len(cnts) > 0:
            # 找到面积最大的轮廓
            c = max(cnts, key=cv.contourArea)
            # 使用最小外接圆圈出面积最大的轮廓
            ((x, y), radius) = cv.minEnclosingCircle(c)
            # 计算轮廓的矩
            M = cv.moments(c)
            # 计算轮廓的重心
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # 只处理尺寸足够大的轮廓
            if radius > 20:
                print(radius)
                # 画出最小外接圆
                cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                
                #计算每一帧的识别结果相对视野中心的位置
                #按照200像素宽度划分大致方位
                #print(x)

                cv.circle(frame, center, 5, (0, 0, 255), -1)
 
        cv.imshow('frame', frame)
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
    cap.release()
    cv.destroyAllWindows()
 
#hsvtest(3,43,46,10,255,255)#red
hsvtest(26,43,46,34,255,255)#yellow
#hsvtest(35,43,46,77,255,255)#green
#hsvtest(0,0,221,180,30,255)#white
#hsvtest(15,90,130,22,200,200)#black