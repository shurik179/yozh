# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT


# Print ifno about AprilTags
# make sure HuskyLens has been cofigured and trained to recognize AprilTags
# also, make sure to choose protocol mode to be I2C in Huskylens general settings
# By default it is set to "auto", which doesn't work very well
#

import time
from huskylens import *
from  yozh import *

bot = Yozh()
camera = Huskylens()

# set both LEDs to Blue
bot.set_leds(BLUE)
# buzz at frequency 440Hz for 1 sec
bot.buzz(440,1.0)
# new messages on display
bot.set_text(1, "Press A to continue")
#wait until user presses button A
# there are two buttons: button_A, button_B
bot.wait_for(BUTTON_A)
bot.clear_display()

while True:
    n=camera.getObjects() # get all recognized objects
    if (n>0): # at least one object in view
        item = camera.receivedObjects[0]
        bot.set_text(1, "Found: ID {}".format(item.ID))
        print("Block with ID {}: size {}x{}, coordinates ({},{})".format(item.ID,item.width, item.height, item.x, item.y))
        bot.set_text(2,"Size {}x{}, \ncoordinates ({},{})".format(item.width, item.height, item.x, item.y))
        bot.set_leds(GREEN)

    else:
        bot.set_leds(BLUE)
        bot.clear_display()
    #time.sleep(0.1)
