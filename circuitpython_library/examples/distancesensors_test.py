# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT
# Testing distnace sensors

import time
from  yozh import *

bot = Yozh()

# set both LEDs to Blue
bot.set_leds(BLUE)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# new messages on display

bot.set_text(1, "Testing distance sensors")

while True:
    left  = bot.distance_L.range
    right = bot.distance_R.range
    bot.set_text(2, "L:{}  R:{}".format(left,right))
    if left<200:
        bot.set_led_L(RED)
    else:
        bot.set_led_L(GREEN)

    if right<200:
        bot.set_led_R(RED)
    else:
        bot.set_led_R(GREEN)
    #time.sleep(0.1)
