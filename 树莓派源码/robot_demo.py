#这个包主要写的是机器人的各种基础动作
from robotpi_movement import Movement

import time


def move_around(time):
    mv=Movement()
    mv.left_ward(-90,8,20,time)
    

turn_speed=5
turn_time=500

def turn_left(speed=turn_speed,time=turn_time):
    mv=Movement()
    mv.turn_left(speed,time)
    return

def turn_right(speed=turn_speed,time=turn_time):
    mv=Movement()
    mv.turn_right(speed,time)
    return

def go_stra(s_speed=10,s_time=500):
    mv=Movement()
    mv.move_forward(s_speed,s_time)
    time.sleep(s_time/1000)
    return

def go_left(speed=30,time=500):
    mv=Movement()
    mv.move_left(speed,time)
    return

def firstgesture():
    mv=Movement()
    mv.FirstGesture()
    return

def secondgesture():
    mv=Movement()
    mv.SecondGesture()
    return

def liftbox():
    mv=Movement()
    mv.LiftBox()
    return

def dropbox():
    mv=Movement()
    mv.DropBox()
    return

def battlemode():
    mv=Movement()
    mv.RobotModeSet()
    print('battle mode!')
    return