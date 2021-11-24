# SPDX-FileCopyrightText: Alexander Kirillov
# SPDX-License-Identifier: CC0-1.0

# Testing basic driving operations

import time
import yozh

RED=[255,0,0]
GREEN=[0,255,0]
BLUE=[0,0,255]

bot = yozh.Yozh()
# initialize display
bot.clear_display()
line1=bot.add_textbox(text_wrap=22, line_spacing=1.0)
line2=bot.add_textbox(text_position=(0,25))
bot.set_text("Yozh initialized!", line1)
time.sleep(1.0)
# show  basic info
bot.set_text("FW version: "+ bot.fw_version(), line1)
voltage = bot.battery()
bot.set_text("Voltage: {}".format(voltage), line2)
# set both LEDs to Blue
bot.set_leds(BLUE)
# wait for 2 sec
time.sleep(2.0)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
bot.configure_PID(maxspeed=4200)
# enable PID control
bot.PID_on()
# new messages on display
bot.set_text("Press button A to continue", line1)
bot.set_text("", line2)
#wait until user presses button A
bot.wait_for(bot.button_A)
bot.buzz(660,1.0)
while True:
    # go forward for 60 cm at 50% speed
    bot.go_forward(60,50)
    bot.turn(90)
    time.sleep(0.5)
