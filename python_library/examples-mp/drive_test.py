# Testing basic driving operations

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
bot.configure_PID(maxspeed=4200)
# enable PID control
bot.PID_on()
# new messages on display
bot.clear_display()
bot.set_text("Press button A \n to continue", 0)
#wait until user presses button A
bot.wait_for(bot.button_A)
bot.buzz(660,1.0)
while True:
    # go forward for 60 cm at 50% speed
    bot.go_forward(60,50)
    bot.turn(90)
    distance = bot.get_distance()
    bot.clear_display()
    bot.set_text("dist: {}".format(distance))
    sleep(0.5)
