# SPDX-FileCopyrightText: Alexander Kirillov
# SPDX-License-Identifier: CC0-1.0

# Testing front distance sensors

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


bot.set_text("Testing distance sensors", line1)

while True:
    left  = bot.distance_L.range
    right = bot.distance_R.range
    bot.set_text("L:{}  R:{}".format(left,right), line2)
    if left<200:
        bot.set_led_L(RED)
    else:
        bot.set_led_L(GREEN)

    if right<200:
        bot.set_led_R(RED)
    else:
        bot.set_led_R(GREEN)
    #time.sleep(0.1)
