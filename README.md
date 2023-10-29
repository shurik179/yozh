# Yozh Robot
Yozh is a small robot based on Pololu's Zumo chassis but programmable in CircuitPython.
It was created by shurik179 for a robotics class at SigmaCamp.
Detailed documentation is available at http://yozh.rtfd.io.

At the moment, it is a work in progress and not ready for public consumption yet

## Status
currently working on version 4

## Project overview
The robot consists of the following components:
* [Zumo chassis](https://www.pololu.com/product/1418) by Pololu
* Two micro metal gearmotors by Pololu ([6V, HP, 75 gear ratio](https://www.pololu.com/product/2215))
* Custom electronics board, containing a slave MCU (SAMD21) preprogrammed with firmware,
  which takes care of all low-level operations such as counting encoder pulses
* Additional boards: reflectance sensor array (for line following), front
  distance sensors, top cover with 64*128 OLED display and user buttons
* [ItsyBitsy RP2040](https://www.adafruit.com/product/4888) by Adafruit, which
  serves as robot brain. It is plugged  into headers   on the main board and
  programmed by the user in CircuitPython, using a provided CircuitPython
  library to communicate with the slave MCU over I2C.




## Structure of this repository
* `docs`: documentation
* `hardware`: design files for the custom electronics boards, BOM, etc.
* `firmware`: bootloader and firmware files
* `circuitpython_library`: Circuit Python user library

## License
Ecept as noted below, all components (hardware, software, documentation) are
copyright by Alexander Kirillov  and are  released under MIT license.
See file LICENSE in this directory for full text of the license.

Circuit Python librabries included in circuitpython_library/lib are copyright by Adafruit, see
https://github.com/adafruit/Adafruit_CircuitPython_Bundle . They are released under MIT License.

Fonts included with Circuit Python library are released under SIL Open Font License.
See LICENSE file in directory circuitpython_library/fonts
