First program
=============

The `CIRCUITPY` drive which was created during installation of CircuitPython on
EPS32-S3  contains a special file, `code.py`. This file always contains
the code of the  current program running on the board. As soon as you turn the
robot on or hit reset, the robot starts  executing this program.


To test the robot, connect it to the computer, using the USB-C connector of the
ESP32-S3. **Make sure the robot switch is
in ON position**. Start  Thonny   editor and open `code.py` file in `CIRCUITPY` drive,
by clicking on it in the navigation pane on the left or using ``File->Open`` menu item.   
Erase everything in that file so it is blank.

Now, use the top part of the navigataion panel to open the  folder with 
examples from Yozh library you downloaded previously. In that folder, 
find the file `basic_test.py` and click on it to open it in another tab of Thonny 
editor. Copy the whole contents of `basic_test.py`
file and then paste it in `code.py` file. 

Now  click on the green ``Run`` button on Thonny toolbar 
to save `code.py` file and run it. The robot will execute your first program!
Look at the OLED screen, read the prompts, press the buttons, and have fun.

The code is amply commented, so it is easy to make changes.


Note: after running the code, or after disconnecting and reconnecting the robot  to the computer, 
you need to again hit the ``Stop`` button for the editor to reconnnect to the robot. 
Try modifying the code (e.g. changing the text printed to screen) and then
re-save it.
