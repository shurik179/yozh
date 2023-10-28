# Yozh Bot servo example

import time
from  yozh import *

bot = Yozh()

# set both LEDs to Blue
bot.set_leds(BLUE)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# new messages on display
bot.set_text(1, "Press button to set servos")
bot.set_text(2, "A and C for max/min")
bot.set_text(3, "B for midpoint")
bot.buzz(660,1.0)
while True:
    #change positions dependingon button pressed
    button=bot.choose_button()
    if button == "A":
        #if button A is pressed - set LEDs blue
        bot.set_servo1(0.0)
        bot.set_servo2(0.0)
        bot.set_leds(BLUE)
    elif button == "C":
        bot.set_servo1(1.0)
        bot.set_servo2(1.0)
        bot.set_leds(RED)
    else:
        bot.set_servo1(0.5)
        bot.set_servo2(0.5)
        bot.set_leds(GREEN)


