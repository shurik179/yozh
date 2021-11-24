# SPDX-FileCopyrightText: Alexander Kirillov
# SPDX-License-Identifier: CC0-1.0

# Basic example of Yozh Bot, with LEDs and buttons

# Import all board pins.
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
line3=bot.add_textbox(text_position=(0,45))
bot.set_text("Yozh initialized!", line1)
time.sleep(1.0)
# show  basic info
bot.set_text("FW version: "+ bot.fw_version(), line1)
voltage = bot.battery()
bot.set_text("Voltage: {}".format(voltage), line2)
# set both LEDs to Blue
bot.set_leds(BLUE)
#turn on line reflectance sensors
bot.linearray_on()
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# wait for 3 sec
time.sleep(3.0)

bot.set_text(" ", line2)
bot.set_text("Place robot partly on black and press button A to calibrate", line1)
bot.wait_for(bot.button_A)
bot.set_leds(RED)
bot.calibrate()
bot.set_leds(BLUE)
bot.set_text("Calibration complete", line1)
time.sleep(2.0)
while True:
    # print raw values
    raw_values = ""
    for i in range(8):
        raw_values+=str(bot.linearray_raw(i))+"; "
    bot.set_text(raw_values, line1)
    # print calibrated values
    cal_values=""
    for i in range(8):
        cal_values+=str(round(bot.linearray_cal(i)))+";"
    bot.set_text(cal_values,line2)
    # print line position
    x = round(bot.line_position_white(),1)
    bot.set_text("Line: {}".format(x), line3)
    if x>0:
        bot.set_leds(RED, GREEN)
    else:
        bot.set_leds(GREEN, RED)
    time.sleep(0.3)
