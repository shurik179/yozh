Serial console
==============
For debugging the program, one needs  to print some
information such as variable values and error messages. Python has built-in command
`print()` which does that. The output of print command is sent to `serial console` -
which in practice just means that it is sent over USB to the computer.

Mu editor has built-in serial console, so you can see these messages. To enable
the console, click on **Serial** icon in the toolbar. The serial console will
appear at the bottom of the screen.

After activating the serial console, you will probably want to restart the program.
The easiest way to do that is by clicking  **Save** again, even if you didn't
make any changes. This will cause the file to be re-saved and program execution restarted.

For more information about using serial console please check Adafruit documentation:
https://learn.adafruit.com/adafruit-itsybitsy-rp2040/connecting-to-the-serial-console .
Among other features it provides is the ability to enter Python commands
interactively in the console, without saving them to a file - this is very
useful for testing various things. This is called REPL (Read-Evaluate-Print Loop);
see https://learn.adafruit.com/adafruit-itsybitsy-rp2040/the-repl for more info. 
