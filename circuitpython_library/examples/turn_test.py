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
# new messages on display

bot.set_text(1,"Press button A to \n calibrate IMU, \nbutton B to skip calibration")
#wait until user presses one of buttons

if (bot.choose_button()=="A"):
    bot.clear_display()
    bot.set_text(1, "Calibrating IMU...")
    bot.IMU_start()
    time.sleep(2.0)
    bot.IMU_calibrate()
    time.sleep(1.0)
    bot.buzz(660,1.0)
    bot.set_text(1, "IMU calibrated")
else:
    #button B was pressed
    bot.clear_display()
    bot.IMU_start()
    time.sleep(2.0)
    bot.set_text(0, "IMU initialized")

if (bot.IMU_status() != 1):
    bot.set_text(3,"IMU failed: {}".format(bot.IMU_status()), font = FONT_BOLD, color = RED)
    while True:
        pass

time.sleep(5.0)
start_yaw = bot.IMU_yaw()

while True:
    for i in range (4):
        bot.turn(90)
        angle = bot.normalize(bot.IMU_yaw()-start_yaw)
        bot.set_text(1, "Yaw: {:.1f}".format(angle),font = FONT_BOLD)
        time.sleep(3)
    for i in range (4):
        bot.turn(-90)
        angle = bot.normalize(bot.IMU_yaw()-start_yaw)
        bot.set_text(1, "Yaw: {:.1f}".format(angle),font = FONT_BOLD)
        time.sleep(3)
