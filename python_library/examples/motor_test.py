# SPDX-FileCopyrightText: Alexander Kirillov
# SPDX-License-Identifier: CC0-1.0

# Basic motors test
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
bot.set_text("Press button A to continue", line1)
bot.set_text("", line2)
#wait until user presses button A
bot.wait_for(bot.button_A)
bot.PID_off()
bot.reset_encoders()
bot.buzz(660,1.0)
bot.set_motors(30,30)
while True:
    bot.get_encoders()
    bot.get_speeds()
    bot.set_text("Encoders:{} {}".format(bot.encoder_L, bot.encoder_R), line1)
    bot.set_text("Speed:    {} {}".format(bot.speed_L, bot.speed_R), line2)
    time.sleep(0.2)
