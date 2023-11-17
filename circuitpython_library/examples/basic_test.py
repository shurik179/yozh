# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT
# Basic example of Yozh Bot use, with LEDs and buttons

import time
from  yozh import *

bot = Yozh()

# set both LEDs to Blue
bot.set_leds(BLUE)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# new messages on display
bot.set_text(1, "Press A to continue")
# wait until user presses button A
# there are two buttons: button_A, button_B
bot.wait_for(BUTTON_A)

bot.set_text(1,"Press B to SWITCH colors")
bot.buzz(660,1.0)
while True:
    #change colors depending on whether button B is pressed
    if bot.is_pressed(BUTTON_B):
        #if button is pressed - set LEDs blue
        bot.set_leds(BLUE)
        # turn on the headlights
        bot.set_lights(100)
    else:
        bot.set_leds(RED)
        bot.set_lights(0)
