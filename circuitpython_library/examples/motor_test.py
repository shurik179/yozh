# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT

# Basic motors test

import time
from  yozh import *

bot = Yozh()

# set both LEDs to Blue
bot.set_leds(BLUE)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# wait for 3 sec
# new messages on display
bot.set_text(1, "Press button A to continue")
#wait until user presses button A
bot.wait_for(BUTTON_A)
bot.reset_encoders()
bot.buzz(660,1.0)
bot.set_motors(70,70)
while True:
    bot.get_encoders()
    bot.get_speeds()
    bot.set_text(1, "Encoders:{} {}".format(bot.encoder_L, bot.encoder_R))
    bot.set_text(2, "Speed:    {} {}".format(bot.speed_L, bot.speed_R))
    time.sleep(0.2)
