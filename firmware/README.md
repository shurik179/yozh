# Yozh  Firmware

This folder  contains the firmware and
necessary support files for Yozh robot.

Since Yozh comes with the firmware pre-installed, most users do not need
any of the files in this directory. You only need to use it if you want to
understand the inner workings of the firmware, or to create your own modified
version of the firmware. Note: the authors of the firmware provide no technical
support for modifying the firmware; do it at your own risk.




## Building the firmware from source
This information is for advanced users only. Use at your own risk!!

It is assumed that you have some experience with Arduino, so the instructions
are brief. This is intentional, to discourage inexperienced users.

To build the firmware from the source, you need the following software installed
on your computer:

1.  Arduino IDE (version 1.8 or later).

2. Board definition files -- see instructions below

3. Required libraries:

   *  FlashStorage

   All of these libraries can be installed using library manager built into Arduino IDE

4. After completing the steps above,  restart the Arduino IDE and select
`Adafruti Crickit M0` in *Tools->Board* menu.

You are now ready to build and upload new firmware from source. Download the
contents of this  repository as a zip file, unpack, and find inside it folder
`firmware/yozh-firmware`. Move it  to Arduino sketchbook folder. Now find in that
folder file  `yozh-firmware.ino` and open it in Arduino IDE. Edit is as you
like and upload to the board in the usual way.

### Board definition files
For step 2 above, you need to install the board definition files for Yozh main
board.  The easiest way to do it is to reuse the board definitions
provided by Adafruit for their Crickit board, just changing some files, as
follows:

1. Install Adafruit's board support package for SAMD-based boards, as described
[here](https://learn.adafruit.com/adafruit-feather-m0-basic-proto/setup). Please
use version 1.5.13, **even if later versions are available** (most likely, using
later versions would also be OK, but it was not tested.)

2. Find the installed package files.  To do this, first find the folder with
Arduino configuration data;  depending on your OS and version of Arduino IDE, it
can be either `<username>\AppData\Local\Arduino15` (Windows),
`<username>\Documents\ArduinoData\` (Windows 10, using Arduino IDE installed
from Windows store), or `/home/<user>/.arduino15/` (Linux).

    Once you found the Arduino configuration data folder, navigate to `\packages\adafruit\hardware\samd\1.5.13\variants\crickit_m0`.

3. Download two files `variant.cpp` and `variant.h` from `boardDefinitions`
folder in this repository and use them to replace the corresponding files in
`crickit_m0` folder.

4. Restart Arduino IDE.
