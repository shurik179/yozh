# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT

# Testing Inertial Motion Unit (IMU)
import time
from  yozh import *

bot = Yozh()

# set both LEDs to Blue
bot.set_leds(BLUE)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
bot.set_text(1,"Press button A to \n calibrate IMU, \nbutton B to skip calibration")

#wait until user presses one of buttons
if (bot.choose_button()=="A"):
    bot.clear_display()
    bot.set_text(1, "Calibrating IMU...")
    bot.IMU_calibrate()
    time.sleep(1.0)
    bot.buzz(660,1.0)
    bot.set_text(1, "IMU calibrated")
else:
    #button B was pressed
    bot.clear_display()
    time.sleep(1.0)
    bot.set_text(0, "IMU initialized")

if (bot.IMU_status() != 1):
    bot.set_text(3,"IMU failed: {}".format(bot.IMU_status()), font = FONT_BOLD, color = RED)
    while True:
        pass


while True:
    bot.set_text(1, "yaw: {}".format(bot.IMU_yaw()))
    bot.set_text(2, "pitch: {}".format(bot.IMU_pitch()))
    bot.set_text(3, "roll: {}".format(bot.IMU_roll()))
    bot.IMU_get_accel()
    bot.set_text(4, "Accel: x:{:.1f} y:{:.1f} z:{:.1f}".format(bot.ax, bot.ay, bot.az))
    time.sleep(0.2)
