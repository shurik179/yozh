# SPDX-FileCopyrightText: Alexander Kirillov
# SPDX-License-Identifier: CC0-1.0

# Example of yozh robot following a line (white on black field)
#


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
line3=bot.add_textbox(text_position=(0,45))
bot.set_text("Yozh initialized!", line1)
time.sleep(1.0)
# show  basic info
bot.set_text("FW version: "+ bot.fw_version(), line1)
voltage = bot.battery()
bot.set_text("Voltage: {}".format(voltage), line2)
bot.PID_off()
# set both LEDs to Blue
bot.set_leds(BLUE)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
#turn on line reflectance sensors
bot.linearray_on()
bot.set_text(" ", line2)
bot.set_text("Place robot partly on black and press button A to calibrate", line1)
bot.wait_for(bot.button_A)
bot.calibrate()
bot.set_text("Calibration complete", line1)
bot.set_text("Press B to continue", line2)
bot.wait_for(bot.button_B)
bot.set_text(" ", line1)
bot.set_text(" ", line2)
bot.set_leds([255,0,255])
speed = 70
Kp = 14.0
while (bot.sensor_on_black(bot.A1) and bot.sensor_on_black(bot.A8)):
    error=bot.line_position_white()
    if error>0:
        bot.set_leds(RED,GREEN)
    else:
        bot.set_leds(GREEN,RED)

    bot.set_motors(speed+Kp*error, speed-Kp*error)

bot.stop_motors()
