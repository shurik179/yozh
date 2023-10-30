# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT

# Find the way out of a maze, using wall-following algorithm. 
# Maze passages (not walls!) are indicated by white line on black field

import time
from  yozh import *

bot = Yozh()

# set both LEDs to Blue
bot.set_leds(BLUE)

#turn on line reflectance sensors
bot.linearray_on()
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
time.sleep(1.0)
bot.set_text(1, "Place robot  on black \nand press button A to calibrate")
bot.wait_for(BUTTON_A)
bot.set_leds(RED)
# lets calibrate both line array sensors and IMU
bot.IMU_calibrate()
bot.calibrate()
bot.set_leds(BLUE)
bot.clear_display()
bot.set_text(1,"Calibration complete")
time.sleep(2.0)
bot.set_text(1, "Place robot at maze start \nand press  A ")
bot.wait_for(BUTTON_A)
bot.set_leds(GREEN)

speed = 70
Kp = 19.0

def go_to_intersection():
    while (bot.sensor_on_black(0) and bot.sensor_on_black(6)):
        error=bot.line_position_white()
        if error is None:
            break #exit the while loop
        if error>0:
            bot.set_leds(RED,GREEN)
        else:
            bot.set_leds(GREEN,RED)
        bot.set_motors(speed+Kp*error, speed-Kp*error)
    # end of while loop - we reached end of the line
    bot.stop_motors()

def check_intersection():
    if bot.all_on_black():
        return (0,0,0)
    else:
        left = False
        right = False
        straight = False
        bot.start_forward(30)
        while (bot.distance_traveled()<3):
            if bot.sensor_on_white(6):
                left = True
            if bot.sensor_on_white(0):
                right = True
        bot.stop_motors()
        straight = not bot.all_on_black()
        bot.set_text(1,"Left: {}".format(left))
        bot.set_text(2,"Straight: {}".format(straight))
        bot.set_text(3,"Right: {}".format(right))
        return (left, straight,right)

while True:
    go_to_intersection()
    bot.set_leds(YELLOW)
    (left,straight, right)=check_intersection()
    #bot.wait_for(BUTTON_A)
    time.sleep(1.0)
    bot.clear_display()
    if left:
        bot.turn(-90)
    elif straight:
        pass
    elif right:
        bot.turn(90)
    else:
        bot.turn(180)  


