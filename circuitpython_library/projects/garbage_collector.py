# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT

# garbage collector


import time
from  yozh import *
from huskylens import *


SERVO_UP = 0.5
SERVO_DOWN = 1.0



bot = Yozh()
camera = Huskylens()


def object_detected():
    left = bot.distance_L.range
    right = bot.distance_R.range
    #bot.set_text(4, f"L: {left} R: {right}")
    if (left>600 and right > 600):
        return(False)
    # to avoid glitches, let's double check
    left = bot.distance_L.range
    right = bot.distance_R.range
    if (left>600 and right >600):
        return(False)
    # looks like we really see something
    return(True)

def turn_to_object():
    if not object_detected():
        # no object found 
        return(False)
    
    if (bot.distance_L.range > bot.distance_R.range):
        # turn clockwise 
        bot.set_motors(30,-30)
        while (bot.distance_L.range > bot.distance_R.range):
            pass
        bot.stop_motors() 

    else:
        # turn counterclockwise 
        bot.set_motors(-30,30)
        while (bot.distance_L.range < bot.distance_R.range):
            pass
        bot.stop_motors()
    return(True)

def get_label_center():
    while (camera.getObjects() == 0):
        pass
    item = camera.receivedObjects[0]
    center_x = item.x  - 160
    return(center_x)

def turn_by_camera():
    x = get_label_center()
    bot.turn(0.3*x, 30)
    bot.stop_motors()

        


# Main code 


# set both LEDs to Blue
bot.set_leds(BLUE)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
bot.set_servo1(SERVO_UP)


bot.set_text(1, "Garbage collector", font = FONT_BOLD)
bot.set_text(2, "Press B to run")
bot.wait_for(BUTTON_B)
bot.set_text(2, " ")
bot.set_motors(25,-25)
while not object_detected():
    pass
# we see an object!
bot.stop_motors()
bot.set_text(2, "Object detected")
bot.set_leds(GREEN)
left = bot.distance_L.range
right = bot.distance_R.range
bot.set_text(4, f"L: {left} R: {right}")
time.sleep(1.0)
turn_to_object()

distance = 500
speed = 30
Kp=0.25
bot.set_text(4, " ")
while distance>180: # distance sensors report larger distances when object is at angle, don't ask me why 
    left = bot.distance_L.range
    right = bot.distance_R.range
    distance = min(left, right)
    bot.set_text(4, f"Distance: {distance}", font = FONT_BOLD)
    error = left - right
    if error > 50:
        error = 50
    elif error <-50:
        error = -50
    bot.set_motors(speed+Kp*error, speed- Kp* error)
    
    
bot.stop_motors()
bot.set_servo1(SERVO_DOWN)
bot.set_lights(100)
# get all recognized objects
while (camera.getObjects() == 0):
    pass

item = camera.receivedObjects[0]
bot.set_text(1, "Found: ID {}".format(item.ID))
bot.set_text(2,"Size {}x{}, \ncoordinates ({},{})".format(item.width, item.height, item.x, item.y))
bot.set_leds(RED)
turn_by_camera()
bot.go_forward(3, 20) 
turn_by_camera()
bot.go_forward(10, 20)
bot.set_servo1(SERVO_UP)
bot.set_leds(GREEN)
bot.buzz(660,1.0)





