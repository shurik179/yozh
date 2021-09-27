# yozh
Small robot based on Pololu's Zumo chassis but programmable in CircuitPython.
Created by shurik179 for a robotics class at SigmaCamp.
Detailed documentation will be available at yozh.rtfd.io

At the moment, it is a work in progress and not ready for public consumption yet

## Project overview
The robot consists of the following components:
* [Zumo chassis](https://www.pololu.com/product/1418) by Pololu
* Two micro metal gearmotors by Pololu ([6V, HP, 75 gear ratio](https://www.pololu.com/product/2215))
* Custom electronics board, containing a slave MCU (SAMD21) pregrogrammed with firmware,
  which takes care of all low-level operations such as counting encoder pulses
* Additional boards: reflectance sensor array (for line follwoing), front
  distance sensors, top cover with 64*128 OLED display and user buttons
* [ItsyBitsy RP2040](https://www.adafruit.com/product/4888) by Adafruit, which serves as robot brain. It is plugged in
into headers   on the main board and programmed by the user in CircuitPython,
using a provided CircuitPython library to communicate with the slave MCU over I2C




## Structure of this repository
* `docs`: documentation
* `hardware`: design files for the custom electronics boards, BOM, etc.
* `firmware`: bootloader and firmware files
* `python_library`: user CircuitPython library
