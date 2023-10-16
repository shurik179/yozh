# Example of Yozh robot following a line (white on black field)

from time import sleep
from yozh import Yozh

RED=[255,0,0]
GREEN=[0,255,0]
BLUE=[0,0,255]
bot = Yozh()

bot.begin()

# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# wait for 1 sec
sleep(1.0)
# new messages on display
bot.clear_display()
bot.set_text("Place robot partly \n on black and\n press button A\n to calibrate", 0)
bot.wait_for(bot.button_A)
bot.clear_display()
bot.set_leds(RED)
bot.calibrate()
bot.set_text("Calibration complete", 0)
sleep(1.0)
bot.set_leds([255,0,255])
bot.clear_display()
bot.set_text("Press button B\n to start", 0)
bot.wait_for(bot.button_B)

bot.clear_display()
bot.set_text("Running...", 0)

speed = 50
Kp = 9.0
# position of white line
pos = 0
while (pos is not None):
    if pos>0:
        bot.set_leds(RED,GREEN)
    else:
        bot.set_leds(GREEN,RED)

    bot.set_motors(speed+Kp*pos, speed-Kp*pos)
    # read new position
    pos=bot.line_position_white()

bot.stop_motors()

bot.clear_display()
bot.set_text("Reached end \n of line", 0)
