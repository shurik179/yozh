# Testing Inertial Motion Unit (IMU)

import time
import yozh

RED=[255,0,0]
GREEN=[0,255,0]
BLUE=[0,0,255]

bot = yozh.Yozh()
# initialize display
bot.clear_display()
line1=bot.add_textbox(text_wrap=22, line_spacing=1.0)
line2=bot.add_textbox(text_position=(0,20))
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
bot.set_text("Press button A to calibrate IMU, button B to skip calibration", line1)
bot.set_text("", line2)
#wait until user presses one of buttons
if (bot.choose_button()=="A"):
    bot.set_text("Calibrating IMU...", line1)
    bot.IMU_start()
    time.sleep(2.0)
    bot.IMU_calibrate()
    time.sleep(1.0)
    bot.buzz(660,1.0)
    bot.set_text("IMU calibrated", line1)
else:
    #button B was pressed
    bot.IMU_start()
    time.sleep(2.0)
    bot.set_text("IMU initialized", line1)
#uncomment the lines below for first run

line3=bot.add_textbox(text_position=(0,35))
line4=bot.add_textbox(text_position=(0,50))

while True:
    bot.set_text("yaw: {}".format(bot.IMU_yaw()), line2)
    bot.set_text("pitch: {}".format(bot.IMU_pitch()), line3)
    bot.set_text("roll: {}".format(bot.IMU_roll()), line4)
    time.sleep(0.2)
