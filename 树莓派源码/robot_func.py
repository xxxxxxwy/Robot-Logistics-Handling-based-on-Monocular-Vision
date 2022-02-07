
import robot_demo
#import colortest
import time
#这个包写的是人脸识别相关函数

import cv2 as cv
import dlib
from imutils import face_utils
import numpy as np
#这个包做的是颜色识别相关的各种函数
# 导入所需模块

import imutils

#hsv
#red (0,43,46,10,255,255)or(156,43,46,180,255,255)
#yellow(26,43,46,34,255,255)
#green(35,43,46,77,255,255)
#white(0,0,221,180,30,255)


    

def FindCOLOR(h1,s1,v1,h2,s2,v2):#输入hsv上限限，返回相对位置（1，-1，0）或者未找到（3）
    # 打开摄像头
    #cap = cv.VideoCapture(0)#解决了一个警告
    #cap = cv.VideoCapture(0,cv.CAP_DSHOW)#解决了一个警告
    time.sleep(1)
    FrameNum=0
    FrameMax=10
    Resultlist=[3]*FrameMax#3代表未发现
    while FrameNum<FrameMax:
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
        #cv.imshow('mask', mask)
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
                # 画出最小外接圆
                cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)  
                #计算每一帧的识别结果相对视野中心的位置
                #按照200像素宽度划分大致方位
                #print(x)                
                if x<=200:
                    Resultlist[FrameNum]=-1
                elif x>400:
                    Resultlist[FrameNum]=1
                else:
                    Resultlist[FrameNum]=0
                # 画出重心
                cv.circle(frame, center, 5, (0, 0, 255), -1)
        FrameNum=FrameNum+1
        #cv.imshow('frame', frame)
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
    #cap.release()
    cv.destroyAllWindows()
    print(Resultlist.count(-1),Resultlist.count(0),Resultlist.count(1),Resultlist.count(3))
    tempmax=max(Resultlist.count(-1),Resultlist.count(0),Resultlist.count(1),Resultlist.count(3))
    if tempmax==Resultlist.count(0):#保证视野中心结果的优先级
        return 0
    if tempmax==Resultlist.count(1):
        return 1
    if tempmax==Resultlist.count(-1):
        return -1
    else:
        return 3
    
def CheckSize(h1,s1,v1,h2,s2,v2):
    time.sleep(1)
    # 打开摄像头
    #cap = cv.VideoCapture(0)#解决了一个警告
    #cap = cv.VideoCapture(0,cv.CAP_DSHOW)#解决了一个警告

    FrameNum=0
    FrameMax=10
    

    while FrameNum<FrameMax:

       
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
 
        #cv.imshow('mask', mask)
 
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
                # 画出最小外接圆
                cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                
               
                # 画出重心
                cv.circle(frame, center, 5, (0, 0, 255), -1)
                
                #if radius>max_r:
                 #   cap.release()
                  #  cv.destroyAllWindows()
                   # return radius
            
        FrameNum=FrameNum+1
        #cv.imshow('frame', frame)
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
    #cap.release()
    cv.destroyAllWindows()
    return radius


def get_descriptors(img):
    #1.人脸检测
    dets = detector(img)
    descriptors=[]
    for k, d in enumerate(dets):
        # 2.关键点检测
        shape = sp(img, d)
        # 3.描述子提取，128D向量
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        # 转换为numpy array
        v = np.array(face_descriptor)
        descriptors.append(v)
    return descriptors

def compare(des_list1,des_list2):
    max_dis=1;
    for i in des_list1:
        for j in des_list2:
            dist = np.linalg.norm(i-j)
            print(dist)
            if max_dis>dist:
                max_dis=dist
    print(max_dis)
    if max_dis<0.4 :
        print("Find !")
        return True
    print("Not find !")
    return False

def takeAphoto(path,num):#Sample:takeAphoto("C:\\Users\\admin\\Desktop\\",2)
    #cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if cv.waitKey(4):
        cv.imwrite(path+str(num)+".jpg",frame)
    #cap.release()

def isSAMEperson(des1,path):
    takeAphoto(path,2)
    img2 = cv.imread(path+str(2)+".jpg",cv.IMREAD_COLOR)
    img2=img2[::-1]
    des2 = get_descriptors(img2)
    if(len(des2)==0):
        return 0
    if(compare(des1, des2)):
        return 2
    return 3

def get_first(path,num):#num=1
    unfinish=True
    des1=None
    while(unfinish):
        takeAphoto(path, num)
        img_1=cv.imread(path+str(1)+".jpg",cv.IMREAD_COLOR)
        img_1=img_1[::-1]
        des1=get_descriptors(img_1)
        if(len(des1)>0):
            unfinish=False
    return des1


def SeekTurn(h1,s1,v1,h2,s2,v2):
    #尽可能使得目标在视野中央
    CountTurn=0
    CountTurnMax=15#旋转一周，说明被遮挡，不可能看见物体 这个参数是经验值，需要现场测试
    while True:
        direction=FindCOLOR(h1,s1,v1,h2,s2,v2)
        if(direction==0):
            return 1
        elif(direction==1):
            robot_demo.turn_left()
        elif(direction==-1):
            robot_demo.turn_right()
        else:
            robot_demo.turn_left(10,500)#大角度旋转，用于搜索
            CountTurn=CountTurn+1
            if(CountTurn>CountTurnMax):
                return 0#视野内不能找到目标


def SeekMove(h1,s1,v1,h2,s2,v2,R):#向着目标前进一段距离，距离取决于大小  
    result=CheckSize(h1,s1,v1,h2,s2,v2)
    #print(result)
    if(result>=R):
        return 1 
    robot_demo.go_stra(10,int(min(3000,(R/result)*500)))
    return 0

def SeekRand():#用于解决NoObj的问题
    robot_demo.go_left()

def CheckObj():#扫描人脸
    while True:    
        #robot_demo.move_around(500)
        result=isSAMEperson(des1, '/home/pi/')
        if(result==2):
            return 2
        elif(result==3):
            while(result!=0):
                robot_demo.move_around(500)
                result=isSAMEperson(des1, '/home/pi/')
                if(result==2):
                    return 2
            return 3
        robot_demo.move_around(500)
       
def LiftBox():
    robot_demo.go_stra(10,10000)
    robot_demo.liftbox()

def DropBox():
    robot_demo.dropbox()

def DealWithColor(h1,s1,v1,h2,s2,v2):
    DoneScan=0#已经完成扫描
    NoObj=0#不可能发现目标
    DoneNear=0#已经接近目标
    DoneCheck=0#已经确定人脸匹配了
    while(DoneScan==0):
        while(NoObj==0 and DoneScan==0):
            result1=SeekTurn(h1,s1,v1,h2,s2,v2)
            if(result1==0):
                NoObj=1
                break
            result2=SeekMove(h1,s1,v1,h2,s2,v2,200)
            if(result2==1):
                DoneNear=1
                break
        if(NoObj==1):
            SeekRand()
            NoObj=0
        if(DoneNear==1):
            result=CheckObj()
            #if(result==0):#因为某些意外，没找到人脸
             #   DoneNear=0
              #  break
            if(result==3):#找到人脸，不匹配
                DoneScan=1
                break
            elif(result==2):#找到人脸，匹配
                DoneScan=1
                DoneCheck=1
                SeekTurn(h1,s1,v1,h2,s2,v2)
                SeekTurn(h1,s1,v1,h2,s2,v2)
                break
    return DoneCheck

def GoWhite(h1,s1,v1,h2,s2,v2,r):
    DoneNear=0
    NoObj=0
    while(DoneNear==0):
        result1=SeekTurn(h1,s1,v1,h2,s2,v2)
        if(result1==0):
            NoObj=1
            break
        result2=SeekMove(h1,s1,v1,h2,s2,v2,r)
        if(result2==1):
            DoneNear=1
            break
        if(NoObj==1):
            SeekRand()



def main():
    DoneCheck=0
    while True:#完成CHECK之后跳出循环
        #DoneCheck=DealWithColor(3,43,46,10,255,255)#red
        #if(DoneCheck==1):
         #   break
        DoneCheck=DealWithColor(35,43,46,77,255,255)#green
        if(DoneCheck==1):
            break
        DoneCheck=DealWithColor(26,43,46,34,255,255)#yellow
        if(DoneCheck==1):
            break
    LiftBox()
    GoWhite(15,90,130,22,200,200,100)
    robot_demo.go_stra(30,8000)
    DropBox()
    #cap.release()


#GoWhite(0,0,221,180,30,255,200)
#hsv
#red (0,43,46,10,255,255)or(156,43,46,180,255,255)
#yellow(26,43,46,34,255,255)
#green(35,43,46,77,255,255)
#white(0,0,221,180,30,255)

cap = cv.VideoCapture(0)
GoWhite(15,90,130,22,200,200,100)
robot_demo.go_stra(30,8000)
DropBox()
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
des1=get_first('/home/pi/',1)
robot_demo.firstgesture()
time.sleep(5)
main()

    

