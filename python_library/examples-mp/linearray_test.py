# line array test

from time import sleep
from yozh import Yozh

RED=[255,0,0]
GREEN=[0,255,0]
BLUE=[0,0,255]
bot = Yozh()

bot.begin()

# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# wait for 3 sec
sleep(3.0)
# new messages on display
bot.clear_display()

bot.set_text("Place robot partly \n on black and\n press button A\n to calibrate", 0)
bot.wait_for(bot.button_A)
bot.clear_display()
bot.set_leds(RED)
bot.calibrate()
bot.set_leds(BLUE)
bot.set_text("Calibration complete", 0)
sleep(2.0)
while True:
    bot.clear_display()
    # print raw values
    raw_values = ""
    for i in range(8):
        raw_values+=str(bot.linearray_raw(i))+";"
        if i==3:
            raw_values+="\n"
    bot.set_text(raw_values, 0)
    # print calibrated values
    cal_values=""
    for i in range(8):
        cal_values+=str(round(bot.linearray_cal(i)))+";"
    bot.set_text(cal_values,2)
    # print line position
    pos = bot.line_position_white()
    if pos is None:
        bot.set_text("No line", 3)
    else:
        x = round(bot.line_position_white(),1)
        bot.set_text("Line: {}".format(x), 3)
        if x>0:
            bot.set_leds(RED, GREEN)
        else:
            bot.set_leds(GREEN, RED)
    sleep(0.3)
