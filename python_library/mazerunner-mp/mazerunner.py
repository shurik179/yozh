# Example of Yozh robot following a line (white on black field)

from time import sleep
from yozh import Yozh

RED=[255,0,0]
GREEN=[0,255,0]
BLUE=[0,0,255]
bot = Yozh()


def go_to_intersection():
    pos = 0
    speed = 50
    Kp = 9.0
    while (pos is not None and bot.sensor_on_black(bot.A1) and bot.sensor_on_black(bot.A8)):
            bot.set_motors(speed+Kp*pos, speed-Kp*pos)
            # read new position
            pos=bot.line_position_white()
    bot.stop_motors()

def check_intersection():
    # go forward while checking for intersection lines
    bot.reset_encoders()
    path_left = False
    path_right = False
    path_forward = False
    bot.set_motors(30,30)
    while bot.get_distance()<5:
        if bot.sensor_on_white(bot.A1):
            path_right = True
        if bot.sensor_on_white(bot.A8):
            path_left = True
    if (not bot.all_on_black):
        path_forward = True
    bot.set_leds




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
bot.clear_display()
bot.set_text("Press button B\n to start", 0)
bot.wait_for(bot.button_B)

while True:
    go_to_intersection()
    bot.buzz(660,1.0)
