# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT

# Obstacle avoidance

# FIXME - still need to be updated 

import time
import yozh

RED=[255,0,0]
GREEN=[0,255,0]
BLUE=[0,0,255]

bot = yozh.Yozh()
# initialize display
bot.clear_display()
line1=bot.add_textbox(text_wrap=23, line_spacing=1.0)
line2=bot.add_textbox(text_position=(0,25))
bot.set_text("Yozh initialized!", line1)
time.sleep(1.0)
# show  basic info
bot.set_text("FW version: "+ bot.fw_version(), line1)
voltage = bot.battery()
bot.set_text("Voltage: {}".format(voltage), line2)
# set both LEDs to Blue
bot.set_leds(BLUE)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# wait for 3 sec
time.sleep(3.0)


bot.set_text("Testing Obstacle avoidance", line1)
bot.set_text("Press B to run", line2)
bot.wait_for(bot.button_B)
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
