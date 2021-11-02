First program
=============

The `CIRCUITPY` drive which was created during installation of CircuitPython on
ItsyBitsy RP2040 contains a special file, `code.py`. This file always contains
the code of the  current program running on the board. As soon as you turn the
robot on or hit reset, the robot starts  executing this program.

If you edit this file with Mu editor (or any other editor), the robot
automatically restarts code execution as soon as the file is saved. You **do not**
need to hit reset button or disconnect the robot from the computer.

It also means that if you write a program that involves the robot moving, you
probably want to put a code that waits  for press of a button in your
program - otherwise, your robot will start motion while still connected by USB
cable to the computer, which is probably not what you want.

To test the robot, connect it to the computer; make sure the robot switch is
in ON position. Start the Mu  editor and open `code.py` file in CircuitPython drive,
using **Load** button.  Erase everything in that file so it is blank.

Now, find the folder with examples from Yozh library you downloaded previously.
In that folder, find the file `basic_test.py`and open it in another tab of Mu
editor, again using **Load** button. Copy the whole contents of `basic_test.py`
file and then paste it in `code.py` file. (Unfortunately, Mu doesn't have
*Save as* command, so you must use copy-and-paste.)

Now save `code.py` file and your robot will execute your first program!
Look at the OLED screen, read the prompts, press the buttons, and have fun.

The code is amply commented, so it is easy to make changes.
Try modifying the code (e.g. changing the text printed to screen) and then
re-save it.
