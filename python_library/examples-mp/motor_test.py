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
# new messages on display
bot.clear_display()
bot.set_text("Press button A \n to continue", 0)
#wait until user presses button A
bot.wait_for(bot.button_A)
bot.PID_off()
bot.reset_encoders()
bot.buzz(660,1.0)
bot.set_motors(30,30)
while True:
    bot.get_encoders()
    bot.get_speeds()
    bot.clear_display()
    bot.set_text("Enc: {} {}".format(bot.encoder_L, bot.encoder_R), 0)
    bot.set_text("Speed:{} {}".format(bot.speed_L, bot.speed_R), 1)
    sleep(0.2)
