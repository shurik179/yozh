# Yozh Bot servo example

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
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# wait for 3 sec
time.sleep(3.0)
# new messages on display
bot.set_text("Press A or B to set servos", line1)
bot.set_text("", line2)
bot.buzz(660,1.0)
while True:
    #change colors depending on whether button B is pressed
    if bot.is_pressed(bot.button_B):
        #if button is pressed - set LEDs blue
        bot.set_servo1(0.0)
        bot.set_servo2(0.0)
        bot.set_leds(BLUE)
    elif bot.is_pressed(bot.button_A):
        bot.set_servo1(1.0)
        bot.set_servo2(1.0)
        bot.set_leds(RED)
