# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT

# Example of Yozh robot following a line (white on black field)

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
bot.set_text(1," ")

speed = 70
Kp = 19.0

while True:
    bot.set_leds(YELLOW)
    bot.set_text(2,"Press B to start", font = FONT_BOLD)
    bot.wait_for(BUTTON_B)
    bot.set_leds(GREEN)
    #start driving
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
