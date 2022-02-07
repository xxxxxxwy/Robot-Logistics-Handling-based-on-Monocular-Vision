
import robot_demo
import colortest_battle
import time
#这个包写的是人脸识别相关函数
import cv2
import dlib
from imutils import face_utils
import numpy as np


def SeekTurn(h1,s1,v1,h2,s2,v2):
    #尽可能使得目标在视野中央
    robot_demo.secondgesture()
    CountTurn=0
    CountTurnMax=7#旋转一周，说明被遮挡，不可能看见物体 这个参数是经验值，需要现场测试
    while True:
        direction=colortest_battle.FindCOLOR(h1,s1,v1,h2,s2,v2)
        
        if(direction==0):
            return 1
        elif(direction==1):
            robot_demo.turn_left(10,200)
        elif(direction==-1):
            robot_demo.turn_right(10,200)
        else:
            robot_demo.turn_right(25,500)#大角度旋转，用于搜索
            CountTurn=CountTurn+1
            if(CountTurn>CountTurnMax):
                return 0#视野内不能找到目标


def SeekMove(h1,s1,v1,h2,s2,v2,R):#向着目标前进一段距离，距离取决于大小
    robot_demo.secondgesture()
    result=colortest_battle.CheckSize(h1,s1,v1,h2,s2,v2)
    if(result>=R):
        return 1
    robot_demo.go_stra(25,500)
    return 0

def SeekRand():#用于解决NoObj的问题
    robot_demo.go_left()

def GoWhite(h1,s1,v1,h2,s2,v2,r):
    robot_demo.move_around(1000)
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

def battle():
    robot_demo.battlemode()
    while(1): 
        try:
            GoWhite(0,0,0,180,255,30,100)
            robot_demo.secondgesture()
            robot_demo.move_around(1000)
        except:
            continue
    
        

#hsv
#red (0,43,46,10,255,255)or(156,43,46,180,255,255)
#yellow(26,43,46,34,255,255)
#green(35,43,46,77,255,255)
#white(0,0,221,180,30,255)

battle()
   
#robot_demo.firstgesture()
