# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT

# Testing reflectance array
import time
from  yozh import *

bot = Yozh()

# set both LEDs to Blue
bot.set_leds(BLUE)

#turn on line reflectance sensors
bot.linearray_on()
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# wait for 3 sec
time.sleep(1.0)
bot.set_text(1, "Place robot  on black \nand press button A to calibrate")
bot.wait_for(BUTTON_A)
bot.set_leds(RED)
bot.calibrate()
bot.set_leds(BLUE)
bot.clear_display()
bot.set_text(1,"Calibration complete")
time.sleep(2.0)
while True:
    # print raw values
    raw_values = ""
    for i in range(7):
        raw_values+=str(bot.linearray_raw(i))+"; "
    bot.set_text(1, raw_values, font = FONT_SMALL)
    # print calibrated values
    cal_values=""
    for i in range(7):
        cal_values+=str(round(bot.linearray_cal(i)))+";"
    bot.set_text(2,cal_values,  font = FONT_SMALL)
    # print line position
    x = round(bot.line_position_white(),1)
    bot.set_text(4, "Line: {}".format(x))
    if x>0:
        bot.set_leds(RED, GREEN)
    else:
        bot.set_leds(GREEN, RED)
    time.sleep(0.3)
