# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT

# Obstacle avoidance


import time
from  yozh import *

bot = Yozh()

# set both LEDs to Blue
bot.set_leds(BLUE)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# wait for 3 sec
time.sleep(2.0)


bot.set_text(1, "Testing obstacle avoidance")
bot.set_text(2, "Press B to run")
bot.wait_for(BUTTON_B)
while True:
    left  = bot.distance_L.range
    right = bot.distance_R.range
    obstacle_left = (left<200)
    obstacle_right = (right<200)
    if (obstacle_left and obstacle_right):
        bot.set_leds(RED)
        bot.turn(180)
    elif (obstacle_left):
        bot.set_leds(RED, GREEN)
        bot.turn(45)
    elif (obstacle_right):
        bot.set_leds(GREEN,RED)
        bot.turn(-45)
    else:
        bot.set_leds(GREEN)
        bot.set_motors(40,40)
